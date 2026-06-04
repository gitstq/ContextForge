"""
Main ContextCompressor class - the primary API for the library.
"""

from typing import Optional, Union, List
from .models import (
    CompressionConfig,
    CompressionResult,
    CompressionLevel,
    ContentType,
)
from .pipeline import CompressionPipeline
from .detector import ContentDetector


class ContextCompressor:
    """
    Main entry point for ContextForge compression engine.

    Provides a simple API for compressing LLM context including
    tool outputs, logs, files, and RAG chunks.

    Examples:
        >>> compressor = ContextCompressor()
        >>> result = compressor.compress(log_text)
        >>> print(result.compressed_text)
        >>> print(f"Saved {result.stats.tokens_saved} tokens")

        >>> # With custom config
        >>> config = CompressionConfig(level=CompressionLevel.AGGRESSIVE)
        >>> result = compressor.compress(text, config=config)
    """

    def __init__(self, config: Optional[CompressionConfig] = None):
        """
        Initialize the compressor.

        Args:
            config: Optional compression configuration. Uses defaults if not provided.
        """
        self.config = config or CompressionConfig()
        self._pipeline = CompressionPipeline(self.config)

    def compress(
        self,
        text: str,
        config: Optional[CompressionConfig] = None,
        content_type: Optional[Union[str, ContentType]] = None,
        level: Optional[Union[str, CompressionLevel]] = None,
    ) -> CompressionResult:
        """
        Compress the given text.

        Args:
            text: The text to compress.
            config: Optional configuration override.
            content_type: Override content type detection ('log', 'json', 'code', etc.).
            level: Override compression level ('light', 'balanced', 'aggressive').

        Returns:
            CompressionResult with compressed text and statistics.
        """
        if not text or not text.strip():
            return CompressionResult(
                compressed_text=text or "",
                original_text=text or "",
            )

        # Build effective config
        effective_config = self._merge_config(config, content_type, level)

        # Run pipeline
        return self._pipeline.execute(text, effective_config)

    def compress_file(
        self,
        file_path: str,
        encoding: str = "utf-8",
        config: Optional[CompressionConfig] = None,
    ) -> CompressionResult:
        """
        Compress the contents of a file.

        Args:
            file_path: Path to the file to compress.
            encoding: File encoding (default: utf-8).
            config: Optional configuration override.

        Returns:
            CompressionResult with compressed text and statistics.
        """
        with open(file_path, 'r', encoding=encoding) as f:
            text = f.read()

        result = self.compress(text, config=config)
        result.metadata["source_file"] = file_path
        return result

    def compress_batch(
        self,
        texts: List[str],
        config: Optional[CompressionConfig] = None,
    ) -> List[CompressionResult]:
        """
        Compress multiple texts in batch.

        Args:
            texts: List of texts to compress.
            config: Optional configuration override.

        Returns:
            List of CompressionResult objects.
        """
        return [self.compress(text, config=config) for text in texts]

    def detect_type(self, text: str) -> ContentType:
        """
        Detect the content type of the given text.

        Args:
            text: The text to analyze.

        Returns:
            Detected ContentType enum value.
        """
        return ContentDetector.detect(text)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the token count for the given text.

        Args:
            text: The text to estimate tokens for.

        Returns:
            Estimated token count.
        """
        return CompressionPipeline._estimate_tokens(text)

    def _merge_config(
        self,
        config: Optional[CompressionConfig],
        content_type: Optional[Union[str, ContentType]],
        level: Optional[Union[str, CompressionLevel]],
    ) -> CompressionConfig:
        """Merge base config with overrides."""
        effective = CompressionConfig(
            level=self.config.level,
            content_type=self.config.content_type,
            preserve_line_numbers=self.config.preserve_line_numbers,
            preserve_code_blocks=self.config.preserve_code_blocks,
            preserve_json_structure=self.config.preserve_json_structure,
            max_output_tokens=self.config.max_output_tokens,
            min_compression_ratio=self.config.min_compression_ratio,
            enable_semantic=self.config.enable_semantic,
            enable_structural=self.config.enable_structural,
            enable_regex=self.config.enable_regex,
            enable_dedup=self.config.enable_dedup,
            enable_template=self.config.enable_template,
            custom_patterns=self.config.custom_patterns.copy(),
            sensitive_patterns=self.config.sensitive_patterns.copy(),
            language_hints=self.config.language_hints.copy(),
        )

        if config:
            for key, value in vars(config).items():
                if value is not None and not (isinstance(value, list) and not value):
                    setattr(effective, key, value)

        if content_type:
            if isinstance(content_type, str):
                effective.content_type = ContentType(content_type.lower())
            else:
                effective.content_type = content_type

        if level:
            if isinstance(level, str):
                effective.level = CompressionLevel(level.lower())
            else:
                effective.level = level

        return effective
