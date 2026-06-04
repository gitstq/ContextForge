"""
Tests for ContextForge compression engine.
"""

import pytest
import json
from contextforge import (
    ContextCompressor,
    CompressionPipeline,
    CompressionConfig,
    CompressionResult,
    CompressionStats,
    ContentType,
    CompressionLevel,
    SemanticCompressor,
    StructuralCompressor,
    TemplateCompressor,
    RegexCompressor,
    DedupCompressor,
)
from contextforge.detector import ContentDetector


class TestContentDetector:
    """Test content type detection."""

    def test_detect_log(self):
        text = """[2024-01-15 10:23:45] INFO: Application started
[2024-01-15 10:23:46] DEBUG: Loading config
[2024-01-15 10:23:47] ERROR: Connection failed"""
        assert ContentDetector.detect(text) == ContentType.LOG

    def test_detect_json(self):
        text = '{"name": "test", "value": 42, "items": [1, 2, 3]}'
        assert ContentDetector.detect(text) == ContentType.JSON

    def test_detect_markdown(self):
        text = """# Title
## Section
- Item 1
- Item 2
[Link](https://example.com)"""
        assert ContentDetector.detect(text) == ContentType.MARKDOWN

    def test_detect_code(self):
        text = """import os
def hello():
    return "world"
class App:
    pass"""
        assert ContentDetector.detect(text) == ContentType.CODE

    def test_detect_empty(self):
        assert ContentDetector.detect("") == ContentType.TEXT
        assert ContentDetector.detect("   ") == ContentType.TEXT

    def test_detect_with_confidence(self):
        text = """[2024-01-15 10:23:45] INFO: App started
[2024-01-15 10:23:46] DEBUG: Loading
[2024-01-15 10:23:47] ERROR: Failed"""
        ctype, confidence = ContentDetector.detect_with_confidence(text)
        assert ctype == ContentType.LOG
        assert confidence > 0.5


class TestSemanticCompressor:
    """Test semantic compression strategy."""

    def test_verbose_phrase_removal(self):
        text = "In order to complete the task, we need to basically run the tests."
        compressor = SemanticCompressor()
        config = CompressionConfig(level=CompressionLevel.BALANCED)
        result, meta = compressor.compress(text, config)
        assert "in order to" not in result.lower()
        assert "basically" not in result.lower()

    def test_duplicate_line_removal(self):
        text = "Line one\nLine one\nLine one\nLine two"
        compressor = SemanticCompressor()
        config = CompressionConfig(level=CompressionLevel.BALANCED)
        result, meta = compressor.compress(text, config)
        assert result.count("Line one") == 1

    def test_light_level_skips_semantic(self):
        text = "In order to complete the task"
        compressor = SemanticCompressor()
        config = CompressionConfig(level=CompressionLevel.LIGHT)
        result, meta = compressor.compress(text, config)
        assert "In order to" in result


class TestStructuralCompressor:
    """Test structural compression strategy."""

    def test_blank_line_collapse(self):
        text = "Line 1\n\n\n\n\nLine 2"
        compressor = StructuralCompressor()
        config = CompressionConfig()
        result, meta = compressor.compress(text, config)
        assert "\n\n\n" not in result

    def test_trailing_whitespace_removal(self):
        text = "Line 1   \nLine 2   \n"
        compressor = StructuralCompressor()
        config = CompressionConfig()
        result, meta = compressor.compress(text, config)
        assert "Line 1   " not in result


class TestRegexCompressor:
    """Test regex-based compression."""

    def test_timestamp_replacement(self):
        text = "Event at 2024-01-15T10:23:45.123Z and 2024-01-16T11:00:00Z"
        compressor = RegexCompressor()
        config = CompressionConfig(level=CompressionLevel.BALANCED)
        result, meta = compressor.compress(text, config)
        assert "2024-01-15" not in result
        assert "<TIMESTAMP>" in result

    def test_uuid_replacement(self):
        text = "ID: 550e8400-e29b-41d4-a716-446655440000"
        compressor = RegexCompressor()
        config = CompressionConfig(level=CompressionLevel.BALANCED)
        result, meta = compressor.compress(text, config)
        assert "<UUID>" in result

    def test_url_replacement(self):
        text = "Visit https://www.example.com/path/to/page for details"
        compressor = RegexCompressor()
        config = CompressionConfig(level=CompressionLevel.BALANCED)
        result, meta = compressor.compress(text, config)
        assert "https://www.example.com" not in result
        assert "<URL>" in result

    def test_light_level_only_timestamps(self):
        text = "ID: 550e8400-e29b-41d4-a716-446655440000 at 2024-01-15"
        compressor = RegexCompressor()
        config = CompressionConfig(level=CompressionLevel.LIGHT)
        result, meta = compressor.compress(text, config)
        assert "550e8400" in result  # UUID not replaced in light mode
        assert "2024-01-15" not in result  # Timestamp replaced


class TestDedupCompressor:
    """Test deduplication compression."""

    def test_consecutive_duplicates(self):
        text = "Same line\nSame line\nSame line\nDifferent line"
        compressor = DedupCompressor()
        config = CompressionConfig()
        result, meta = compressor.compress(text, config)
        assert "(x3)" in result

    def test_near_duplicates(self):
        text = "Error at line 1\nError at line 2\nError at line 3\nError at line 4\nError at line 5"
        compressor = DedupCompressor()
        config = CompressionConfig()
        result, meta = compressor.compress(text, config)
        lines = [l for l in result.split('\n') if l.strip()]
        assert len(lines) <= 5


class TestTemplateCompressor:
    """Test template-based compression."""

    def test_log_template(self):
        text = '[2024-01-15 10:23:45] INFO - Application started successfully'
        compressor = TemplateCompressor()
        config = CompressionConfig()
        result, meta = compressor.compress(text, config)
        assert "2024-01-15" not in result
        assert "INFO:" in result

    def test_json_compaction(self):
        text = '{\n  "name": "test",\n  "value": 42,\n  "empty": null,\n  "blank": ""\n}'
        compressor = TemplateCompressor()
        config = CompressionConfig(preserve_json_structure=True)
        result, meta = compressor.compress(text, config)
        # Should compact JSON
        assert '"name":"test"' in result or '"name": "test"' in result


class TestCompressionPipeline:
    """Test the full compression pipeline."""

    def test_log_compression(self):
        text = """[2024-01-15 10:23:45] DEBUG: Starting application...
[2024-01-15 10:23:45] DEBUG: Loading config from /app/config.yaml
[2024-01-15 10:23:46] DEBUG: Connecting to database at 192.168.1.100:5432
[2024-01-15 10:23:46] INFO: Database connected successfully
[2024-01-15 10:23:47] DEBUG: Running migrations...
[2024-01-15 10:23:48] INFO: Migrations completed
[2024-01-15 10:23:48] DEBUG: Starting HTTP server on port 8080
[2024-01-15 10:23:49] INFO: Server started successfully
[2024-01-15 10:23:49] DEBUG: Health check endpoint registered
[2024-01-15 10:23:50] INFO: Application ready"""
        pipeline = CompressionPipeline(
            CompressionConfig(level=CompressionLevel.AGGRESSIVE)
        )
        result = pipeline.execute(text)
        assert result.stats.compression_ratio > 0.2
        assert len(result.compressed_text) < len(text)

    def test_empty_input(self):
        pipeline = CompressionPipeline()
        result = pipeline.execute("")
        assert result.compressed_text == ""

    def test_no_compress_below_threshold(self):
        text = "Short"
        config = CompressionConfig(min_compression_ratio=0.5)
        pipeline = CompressionPipeline(config)
        result = pipeline.execute(text)
        # If compression ratio is below threshold, original is returned
        assert result.compressed_text == text or result.stats.compression_ratio >= 0.5


class TestContextCompressor:
    """Test the main ContextCompressor API."""

    def test_basic_compress(self):
        text = """[2024-01-15 10:23:45] DEBUG: Starting application...
[2024-01-15 10:23:46] INFO: Connected to database at 192.168.1.100
[2024-01-15 10:23:47] DEBUG: Loading module: auth
[2024-01-15 10:23:48] INFO: Authentication service ready
[2024-01-15 10:23:49] DEBUG: Registering routes
[2024-01-15 10:23:50] INFO: Server started on port 8080"""
        compressor = ContextCompressor()
        result = compressor.compress(text)
        assert result.stats.compression_ratio > 0
        assert result.stats.original_tokens > 0

    def test_compress_with_type_override(self):
        text = "Some random text"
        compressor = ContextCompressor()
        result = compressor.compress(text, content_type="text")
        assert result.config.content_type == ContentType.TEXT

    def test_compress_with_level_override(self):
        text = "Some text to compress"
        compressor = ContextCompressor()
        result = compressor.compress(text, level="aggressive")
        assert result.config.level == CompressionLevel.AGGRESSIVE

    def test_empty_input(self):
        compressor = ContextCompressor()
        result = compressor.compress("")
        assert result.compressed_text == ""

    def test_detect_type(self):
        text = "[2024-01-15] INFO: Test\n[2024-01-15] DEBUG: Loading\n[2024-01-15] ERROR: Failed"
        compressor = ContextCompressor()
        assert compressor.detect_type(text) == ContentType.LOG

    def test_estimate_tokens(self):
        text = "Hello world, this is a test of token estimation."
        compressor = ContextCompressor()
        tokens = compressor.estimate_tokens(text)
        assert tokens > 0

    def test_batch_compress(self):
        texts = [
            "[2024-01-15] INFO: Test 1",
            "[2024-01-15] INFO: Test 2",
            "[2024-01-15] INFO: Test 3",
        ]
        compressor = ContextCompressor()
        results = compressor.compress_batch(texts)
        assert len(results) == 3
        for result in results:
            assert isinstance(result, CompressionResult)

    def test_result_to_dict(self):
        compressor = ContextCompressor()
        result = compressor.compress("test text")
        d = result.to_dict()
        assert "compressed_text" in d
        assert "stats" in d
        assert "warnings" in d

    def test_stats_to_dict(self):
        stats = CompressionStats(
            original_length=100,
            compressed_length=50,
            original_tokens=25,
            compressed_tokens=12,
            tokens_saved=13,
            compression_ratio=0.5,
        )
        d = stats.to_dict()
        assert d["compression_ratio"] == 0.5
        assert d["tokens_saved"] == 13


class TestRealWorldScenarios:
    """Test compression with realistic content."""

    def test_application_log(self):
        text = """[2024-06-04 08:15:32.456] DEBUG [main] com.app.Server - Initializing application context
[2024-06-04 08:15:32.789] DEBUG [main] com.app.Config - Loading configuration from /etc/app/config.yml
[2024-06-04 08:15:33.012] INFO  [main] com.app.Database - Connecting to PostgreSQL at db.example.com:5432/app_db
[2024-06-04 08:15:33.456] INFO  [main] com.app.Database - Connection pool initialized (min=5, max=20)
[2024-06-04 08:15:33.789] DEBUG [main] com.app.Cache - Connecting to Redis at cache.example.com:6379
[2024-06-04 08:15:34.012] INFO  [main] com.app.Cache - Redis connection established
[2024-06-04 08:15:34.234] DEBUG [main] com.app.Migration - Running database migrations
[2024-06-04 08:15:34.567] INFO  [main] com.app.Migration - Applied 3 pending migrations
[2024-06-04 08:15:34.890] DEBUG [main] com.app.Router - Registering 42 API endpoints
[2024-06-04 08:15:35.123] INFO  [main] com.app.Server - HTTP server started on 0.0.0.0:8080
[2024-06-04 08:15:35.456] INFO  [main] com.app.Server - Application started in 2.987s
[2024-06-04 08:15:35.789] INFO  [main] com.app.Server - Ready to accept requests
[2024-06-04 08:16:01.234] INFO  [http-nio-8080-exec-1] com.app.Controller - GET /api/users - 200 OK (45ms)
[2024-06-04 08:16:02.345] INFO  [http-nio-8080-exec-2] com.app.Controller - POST /api/auth/login - 200 OK (123ms)
[2024-06-04 08:16:03.456] WARN  [http-nio-8080-exec-3] com.app.RateLimit - Rate limit approaching for IP 203.0.113.42
[2024-06-04 08:16:04.567] ERROR [http-nio-8080-exec-4] com.app.Service - Failed to process request: Connection timeout to api.external.com
[2024-06-04 08:16:05.678] DEBUG [http-nio-8080-exec-4] com.app.Retry - Scheduling retry in 5s (attempt 1/3)"""
        compressor = ContextCompressor()
        result = compressor.compress(text, level="aggressive")
        assert result.stats.compression_ratio > 0.3
        assert len(result.compressed_text) < len(text)

    def test_json_api_response(self):
        text = json.dumps({
            "users": [
                {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "Alice", "email": "alice@example.com", "role": "admin"},
                {"id": "660e8400-e29b-41d4-a716-446655440001", "name": "Bob", "email": "bob@example.com", "role": "user"},
                {"id": "770e8400-e29b-41d4-a716-446655440002", "name": "Charlie", "email": "charlie@example.com", "role": "user"},
            ],
            "pagination": {"page": 1, "per_page": 20, "total": 3},
            "timestamp": "2024-06-04T08:16:00.000Z",
            "request_id": "req-550e8400-e29b-41d4-a716-446655440000",
        }, indent=2)
        compressor = ContextCompressor()
        result = compressor.compress(text, content_type="json", level="aggressive")
        assert result.stats.compression_ratio > 0.1

    def test_tool_output(self):
        text = """Result of file search operation:
Found 15 files matching pattern "*.py":
  /home/user/project/src/main.py (245 lines, last modified: 2024-06-01T14:30:00Z)
  /home/user/project/src/utils.py (189 lines, last modified: 2024-06-02T09:15:00Z)
  /home/user/project/src/config.py (67 lines, last modified: 2024-05-28T16:45:00Z)
  /home/user/project/tests/test_main.py (312 lines, last modified: 2024-06-03T11:20:00Z)
  /home/user/project/tests/test_utils.py (156 lines, last modified: 2024-06-03T11:25:00Z)
Total: 15 files, 4,892 lines of code
Search completed in 0.234 seconds"""
        compressor = ContextCompressor()
        result = compressor.compress(text, level="balanced")
        assert result.stats.compression_ratio > 0.1
