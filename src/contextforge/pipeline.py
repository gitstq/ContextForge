"""
Compression pipeline - orchestrates multiple compression strategies.
"""

import time
from typing import List, Optional
from .models import (
    CompressionConfig,
    CompressionResult,
    CompressionStats,
    CompressionLevel,
    ContentType,
)
from .strategies import (
    BaseStrategy,
    SemanticCompressor,
    StructuralCompressor,
    TemplateCompressor,
    RegexCompressor,
    DedupCompressor,
)
from .detector import ContentDetector


class CompressionPipeline:
    """
    Orchestrates multiple compression strategies in sequence.
    Automatically selects optimal strategies based on content type and config.
    """

    def __init__(self, config: Optional[CompressionConfig] = None):
        self.config = config or CompressionConfig()
        self._strategies: List[BaseStrategy] = []
        self._build_pipeline()

    def _build_pipeline(self):
        """Build the strategy pipeline based on configuration."""
        self._strategies = []

        # Order matters: dedup first, then template, regex, semantic, structural last
        if self.config.enable_dedup:
            self._strategies.append(DedupCompressor())

        if self.config.enable_template:
            self._strategies.append(TemplateCompressor())

        if self.config.enable_regex:
            self._strategies.append(RegexCompressor())

        if self.config.enable_semantic:
            self._strategies.append(SemanticCompressor())

        if self.config.enable_structural:
            self._strategies.append(StructuralCompressor())

    def execute(self, text: str, config: Optional[CompressionConfig] = None) -> CompressionResult:
        """
        Execute the full compression pipeline.
        """
        config = config or self.config
        start_time = time.perf_counter()

        # Detect content type if AUTO
        if config.content_type == ContentType.AUTO:
            detected_type, confidence = ContentDetector.detect_with_confidence(text)
            config.content_type = detected_type
        else:
            confidence = 1.0

        # Estimate original tokens (rough: ~4 chars per token for English, ~2 for CJK)
        original_tokens = self._estimate_tokens(text)

        # Execute each strategy in sequence
        current_text = text
        strategies_used = []
        total_patterns_matched = 0
        total_lines_removed = 0
        all_metadata = {}

        for strategy in self._strategies:
            if strategy.is_applicable(current_text, config):
                compressed, metadata = strategy.compress(current_text, config)
                if compressed != current_text:
                    strategies_used.append(strategy.name)
                    total_patterns_matched += metadata.get("patterns_matched", 0)
                    total_lines_removed += metadata.get("lines_removed", 0)
                    all_metadata[strategy.name] = metadata
                    current_text = compressed

        # Calculate stats
        compressed_tokens = self._estimate_tokens(current_text)
        end_time = time.perf_counter()
        processing_time = (end_time - start_time) * 1000

        original_length = len(text)
        compressed_length = len(current_text)

        compression_ratio = 0.0
        if original_length > 0:
            compression_ratio = 1.0 - (compressed_length / original_length)

        # Check minimum compression ratio
        if compression_ratio < config.min_compression_ratio:
            current_text = text
            compressed_length = original_length
            compressed_tokens = original_tokens
            compression_ratio = 0.0
            strategies_used = []

        # Apply max token limit if set
        warnings = []
        if config.max_output_tokens and compressed_tokens > config.max_output_tokens:
            current_text = self._truncate_to_tokens(current_text, config.max_output_tokens)
            warnings.append(
                f"Output truncated to {config.max_output_tokens} tokens limit"
            )

        stats = CompressionStats(
            original_length=original_length,
            compressed_length=compressed_length,
            original_tokens=original_tokens,
            compressed_tokens=self._estimate_tokens(current_text),
            tokens_saved=original_tokens - self._estimate_tokens(current_text),
            compression_ratio=compression_ratio,
            strategies_used=strategies_used,
            processing_time_ms=processing_time,
            lines_removed=total_lines_removed,
            patterns_matched=total_patterns_matched,
        )

        return CompressionResult(
            compressed_text=current_text,
            original_text=text,
            stats=stats,
            config=config,
            warnings=warnings,
            metadata={
                "detected_type": config.content_type.value,
                "detection_confidence": confidence,
                "strategy_details": all_metadata,
            },
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """
        Estimate token count without external dependencies.
        Uses a simple heuristic: ~4 chars per token for Latin text,
        ~1.5 chars per token for CJK text.
        """
        if not text:
            return 0

        cjk_chars = 0
        latin_chars = 0
        for char in text:
            if '\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u30ff' or '\uac00' <= char <= '\ud7af':
                cjk_chars += 1
            elif char.isalnum() or char in ' \t':
                latin_chars += 1

        cjk_tokens = cjk_chars // 1.5
        latin_tokens = latin_chars // 4
        other_tokens = (len(text) - cjk_chars - latin_chars) // 5

        return int(cjk_tokens + latin_tokens + other_tokens)

    @staticmethod
    def _truncate_to_tokens(text: str, max_tokens: int) -> str:
        """Truncate text to approximately max_tokens tokens."""
        estimated_tokens = CompressionPipeline._estimate_tokens(text)
        if estimated_tokens <= max_tokens:
            return text

        ratio = max_tokens / estimated_tokens
        target_length = int(len(text) * ratio * 0.95)  # 5% safety margin
        truncated = text[:target_length]

        # Try to break at a sentence or line boundary
        last_newline = truncated.rfind('\n')
        last_period = truncated.rfind('. ')
        last_break = max(last_newline, last_period)

        if last_break > target_length * 0.5:
            truncated = truncated[:last_break + 1]

        return truncated + "\n... [truncated]"
