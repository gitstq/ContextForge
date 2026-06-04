"""
Data models for ContextForge compression engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ContentType(Enum):
    """Types of content that can be compressed."""
    AUTO = "auto"
    LOG = "log"
    CODE = "code"
    JSON = "json"
    XML = "xml"
    MARKDOWN = "markdown"
    TEXT = "text"
    TOOL_OUTPUT = "tool_output"
    RAG_CHUNKS = "rag_chunks"
    CONVERSATION = "conversation"
    HTML = "html"
    CSV = "csv"


class CompressionLevel(Enum):
    """Compression aggressiveness levels."""
    LIGHT = "light"       # Safe, minimal compression (~30-50%)
    BALANCED = "balanced" # Good balance of compression and fidelity (~50-70%)
    AGGRESSIVE = "aggressive"  # Maximum compression (~70-90%)
    CUSTOM = "custom"     # User-defined strategy combination


@dataclass
class CompressionConfig:
    """Configuration for the compression engine."""
    level: CompressionLevel = CompressionLevel.BALANCED
    content_type: ContentType = ContentType.AUTO
    preserve_line_numbers: bool = False
    preserve_code_blocks: bool = True
    preserve_json_structure: bool = True
    max_output_tokens: Optional[int] = None
    min_compression_ratio: float = 0.1  # Don't compress if ratio < 10%
    enable_semantic: bool = True
    enable_structural: bool = True
    enable_regex: bool = True
    enable_dedup: bool = True
    enable_template: bool = True
    custom_patterns: list = field(default_factory=list)
    sensitive_patterns: list = field(default_factory=lambda: [
        r'(?i)api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
        r'(?i)password\s*[=:]\s*["\']?[^\s"\']{8,}',
        r'(?i)token\s*[=:]\s*["\']?[a-zA-Z0-9._-]{20,}',
        r'(?i)secret\s*[=:]\s*["\']?[^\s"\']{8,}',
        r'Bearer\s+[a-zA-Z0-9._-]+',
        r'(?:sk|pk|rk|akt)_[a-zA-Z0-9]{20,}',
    ])
    language_hints: list = field(default_factory=list)


@dataclass
class CompressionStats:
    """Statistics about a compression operation."""
    original_length: int = 0
    compressed_length: int = 0
    original_tokens: int = 0
    compressed_tokens: int = 0
    tokens_saved: int = 0
    compression_ratio: float = 0.0
    strategies_used: list = field(default_factory=list)
    processing_time_ms: float = 0.0
    lines_removed: int = 0
    patterns_matched: int = 0

    def to_dict(self) -> dict:
        return {
            "original_length": self.original_length,
            "compressed_length": self.compressed_length,
            "original_tokens": self.original_tokens,
            "compressed_tokens": self.compressed_tokens,
            "tokens_saved": self.tokens_saved,
            "compression_ratio": self.compression_ratio,
            "strategies_used": self.strategies_used,
            "processing_time_ms": round(self.processing_time_ms, 2),
            "lines_removed": self.lines_removed,
            "patterns_matched": self.patterns_matched,
        }


@dataclass
class CompressionResult:
    """Result of a compression operation."""
    compressed_text: str = ""
    original_text: str = ""
    stats: CompressionStats = field(default_factory=CompressionStats)
    config: CompressionConfig = field(default_factory=CompressionConfig)
    warnings: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "compressed_text": self.compressed_text,
            "stats": self.stats.to_dict(),
            "warnings": self.warnings,
            "metadata": self.metadata,
        }
