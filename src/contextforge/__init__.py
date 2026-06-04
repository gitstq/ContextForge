"""
ContextForge - Lightweight LLM Context Intelligent Compression Engine

A zero-dependency (core), cross-platform Python library for intelligently
compressing LLM inputs including tool outputs, logs, files, and RAG chunks.
Achieves 50-90% token reduction while preserving semantic integrity.
"""

__version__ = "1.0.0"
__author__ = "ContextForge Team"
__license__ = "MIT"

from .compressor import ContextCompressor
from .strategies import (
    SemanticCompressor,
    StructuralCompressor,
    TemplateCompressor,
    RegexCompressor,
    DedupCompressor,
)
from .models import (
    CompressionResult,
    CompressionStats,
    CompressionConfig,
    ContentType,
    CompressionLevel,
)
from .pipeline import CompressionPipeline

__all__ = [
    "ContextCompressor",
    "SemanticCompressor",
    "StructuralCompressor",
    "TemplateCompressor",
    "RegexCompressor",
    "DedupCompressor",
    "CompressionResult",
    "CompressionStats",
    "CompressionConfig",
    "ContentType",
    "CompressionLevel",
    "CompressionPipeline",
]
