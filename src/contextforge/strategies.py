"""
Compression strategies for different content types.

Each strategy implements a specific compression technique that can be
chained together in a pipeline for maximum compression.
"""

import re
import json
from abc import ABC, abstractmethod
from typing import Optional
from .models import CompressionConfig, CompressionResult, CompressionStats, CompressionLevel


class BaseStrategy(ABC):
    """Abstract base class for compression strategies."""

    name: str = "base"

    @abstractmethod
    def compress(self, text: str, config: CompressionConfig) -> tuple:
        """
        Compress the given text.
        Returns: (compressed_text, metadata_dict)
        """
        pass

    def is_applicable(self, text: str, config: CompressionConfig) -> bool:
        """Check if this strategy is applicable for the given text."""
        return True


class SemanticCompressor(BaseStrategy):
    """
    Semantic compression: removes redundant information while preserving meaning.
    Handles verbose descriptions, repeated concepts, and filler content.
    """

    name = "semantic"

    # Patterns for semantic redundancy removal
    VERBOSE_PATTERNS = [
        # Redundant qualifiers
        (r'\b(?:absolutely|completely|totally|entirely|utterly|quite|rather|'
         r'very|really|actually|basically|essentially|literally|simply|just)\b\s+', ''),
        # Redundant phrases
        (r'\bin order to\b', 'to'),
        (r'\bdue to the fact that\b', 'because'),
        (r'\bfor the purpose of\b', 'for'),
        (r'\bin the event that\b', 'if'),
        (r'\bat this point in time\b', 'now'),
        (r'\bwith regard to\b', 'about'),
        (r'\bin spite of the fact that\b', 'although'),
        (r'\bon account of\b', 'because'),
        (r'\bin close proximity to\b', 'near'),
        (r'\bhas the ability to\b', 'can'),
        (r'\bis able to\b', 'can'),
        (r'\bmake a decision\b', 'decide'),
        (r'\btake into consideration\b', 'consider'),
        (r'\bcome to a conclusion\b', 'conclude'),
        (r'\bperform an analysis\b', 'analyze'),
        (r'\bprovide a summary of\b', 'summarize'),
        (r'\bcarry out an investigation\b', 'investigate'),
        # Repeated sentences (similar meaning)
        (r'\n(\s*\n){3,}', '\n\n'),  # Multiple blank lines
    ]

    def compress(self, text: str, config: CompressionConfig) -> tuple:
        if config.level == CompressionLevel.LIGHT:
            return text, {}

        compressed = text
        patterns_matched = 0

        for pattern, replacement in self.VERBOSE_PATTERNS:
            new_text = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
            if new_text != compressed:
                patterns_matched += len(re.findall(pattern, compressed, re.IGNORECASE))
                compressed = new_text

        # Remove consecutive duplicate lines
        lines = compressed.split('\n')
        deduped_lines = []
        prev_line = None
        for line in lines:
            stripped = line.strip()
            if stripped and stripped == prev_line:
                continue
            deduped_lines.append(line)
            prev_line = stripped
        compressed = '\n'.join(deduped_lines)

        metadata = {
            "patterns_matched": patterns_matched,
            "verbose_replacements": patterns_matched,
        }
        return compressed, metadata


class StructuralCompressor(BaseStrategy):
    """
    Structural compression: reorganizes content structure for compactness.
    Handles indentation normalization, whitespace collapsing, and structural patterns.
    """

    name = "structural"

    def compress(self, text: str, config: CompressionConfig) -> tuple:
        compressed = text
        lines_removed = 0

        # Normalize excessive indentation
        lines = compressed.split('\n')
        normalized = []
        for line in lines:
            # Reduce indentation to max 4 levels
            stripped = line.lstrip()
            indent_level = min((len(line) - len(stripped)) // 4, 4)
            normalized.append('    ' * indent_level + stripped)
        compressed = '\n'.join(normalized)

        # Collapse multiple blank lines
        compressed = re.sub(r'\n(\s*\n){2,}', '\n\n', compressed)

        # Remove trailing whitespace per line
        lines = compressed.split('\n')
        compressed = '\n'.join(line.rstrip() for line in lines)

        # Remove empty lines at start and end
        compressed = compressed.strip()

        # For code blocks, normalize spacing
        if not config.preserve_code_blocks:
            # Remove comments in code (simple single-line comments)
            lines = compressed.split('\n')
            filtered = []
            for line in lines:
                stripped = line.strip()
                # Skip empty comment lines
                if stripped in ('#', '//', '--', '/*', '*/'):
                    lines_removed += 1
                    continue
                filtered.append(line)
            compressed = '\n'.join(filtered)

        metadata = {"lines_removed": lines_removed}
        return compressed, metadata


class RegexCompressor(BaseStrategy):
    """
    Regex-based compression: applies configurable patterns to remove noise.
    Handles timestamps, URLs, hex values, and other token-heavy patterns.
    """

    name = "regex"

    # Predefined compression patterns
    PATTERNS = {
        "timestamps": [
            (r'\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b', '<TIMESTAMP>'),
            (r'\b\d{2}:\d{2}:\d{2}(?:\.\d+)?\b', '<TIME>'),
            (r'\b\d{4}-\d{2}-\d{2}\b', '<DATE>'),
        ],
        "ids": [
            (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '<UUID>'),
            (r'\b[0-9a-f]{32,}\b', '<HEX_ID>'),
        ],
        "urls": [
            (r'https?://[^\s<>"{}|\\^`\[\]]+', '<URL>'),
        ],
        "numbers": [
            (r'\b\d{10,}\b', '<BIG_NUM>'),
        ],
        "paths": [
            (r'(?:/[\w.-]+){3,}', '<PATH>'),
        ],
        "memory_addresses": [
            (r'\b0x[0-9a-fA-F]{4,16}\b', '<ADDR>'),
        ],
        "version_strings": [
            (r'\b\d+\.\d+\.\d+(?:[-.]\w+)*\b', '<VER>'),
        ],
        "email_like": [
            (r'\b[\w.-]+@[\w.-]+\.\w+\b', '<EMAIL>'),
        ],
        "ip_addresses": [
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>'),
        ],
        "file_hashes": [
            (r'\b[0-9a-fA-F]{40,64}\b', '<HASH>'),
        ],
    }

    def compress(self, text: str, config: CompressionConfig) -> tuple:
        compressed = text
        patterns_matched = 0

        categories_to_apply = []
        if config.level == CompressionLevel.LIGHT:
            categories_to_apply = ["timestamps"]
        elif config.level == CompressionLevel.BALANCED:
            categories_to_apply = ["timestamps", "ids", "urls", "paths", "memory_addresses"]
        elif config.level == CompressionLevel.AGGRESSIVE:
            categories_to_apply = list(self.PATTERNS.keys())

        for category in categories_to_apply:
            for pattern, replacement in self.PATTERNS.get(category, []):
                new_text = re.sub(pattern, replacement, compressed)
                if new_text != compressed:
                    patterns_matched += len(re.findall(pattern, compressed))
                    compressed = new_text

        # Apply custom patterns
        for custom_pattern in config.custom_patterns:
            if isinstance(custom_pattern, dict):
                pattern = custom_pattern.get("pattern", "")
                replacement = custom_pattern.get("replacement", "<REDACTED>")
            else:
                pattern = str(custom_pattern)
                replacement = "<REDACTED>"
            if pattern:
                new_text = re.sub(pattern, replacement, compressed)
                if new_text != compressed:
                    patterns_matched += len(re.findall(pattern, compressed))
                    compressed = new_text

        metadata = {"patterns_matched": patterns_matched}
        return compressed, metadata


class DedupCompressor(BaseStrategy):
    """
    Deduplication compressor: removes duplicate content blocks.
    Handles repeated log entries, duplicate code blocks, and redundant sections.
    """

    name = "dedup"

    def compress(self, text: str, config: CompressionConfig) -> tuple:
        lines = text.split('\n')
        seen_blocks = {}
        result = []
        duplicates_found = 0
        lines_removed = 0

        # Check for consecutive duplicate blocks (3+ identical lines)
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Skip empty lines for dedup check
            if not stripped:
                result.append(line)
                i += 1
                continue

            # Check for consecutive duplicates (same line repeated)
            if i + 2 < len(lines):
                if (lines[i].strip() == lines[i+1].strip() == lines[i+2].strip()
                        and stripped):
                    # Keep first occurrence, note the count
                    count = 1
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == stripped:
                        count += 1
                        j += 1
                    result.append(f"{line} (x{count})")
                    duplicates_found += count - 1
                    lines_removed += count - 1
                    i = j
                    continue

            # Check for near-duplicate lines (same pattern, different values)
            line_hash = self._fuzzy_hash(stripped)
            if line_hash in seen_blocks:
                seen_blocks[line_hash] += 1
                if seen_blocks[line_hash] > 3:  # Allow up to 3 similar lines
                    lines_removed += 1
                    i += 1
                    continue
            else:
                seen_blocks[line_hash] = 1

            result.append(line)
            i += 1

        compressed = '\n'.join(result)

        metadata = {
            "duplicates_found": duplicates_found,
            "lines_removed": lines_removed,
        }
        return compressed, metadata

    def _fuzzy_hash(self, line: str) -> str:
        """Create a fuzzy hash for near-duplicate detection."""
        # Replace numbers and specific values with placeholders
        hashed = re.sub(r'\b\d+\.?\d*\b', 'N', line)
        hashed = re.sub(r'\b[0-9a-f]{8,}\b', 'H', hashed)
        hashed = re.sub(r'["\'][^"\']*["\']', 'S', hashed)
        return hashed


class TemplateCompressor(BaseStrategy):
    """
    Template-based compression: replaces structured content with compact templates.
    Handles log formats, JSON structures, table data, and other structured content.
    """

    name = "template"

    # Log line templates
    LOG_TEMPLATES = [
        # Standard log format: [TIMESTAMP] LEVEL Message
        (r'^\[(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s*'
         r'(DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL|TRACE)\s*'
         r'[-–—]\s*(.+)$',
         None),  # Handled specially: just strip timestamp
        # Syslog format
        (r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+'
         r'(\S+)\s+'
         r'(\S+?):\s*(.+)$',
         None),
        # Java-style log: [TIMESTAMP] LEVEL [thread] package - message
        (r'^\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s*'
         r'(DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL|TRACE)\s*'
         r'\[([^\]]+)\]\s*(.+?)\s*[-–—]\s*(.+)$',
         None),
    ]

    # JSON compression patterns
    JSON_PATTERNS = [
        # Remove null/empty fields
        (r',?\s*"\w+"\s*:\s*null', ''),
        (r',?\s*"\w+"\s*:\s*\{\}', ''),
        (r',?\s*"\w+"\s*:\s*\[\]', ''),
        (r',?\s*"\w+"\s*:\s*""', ''),
    ]

    def compress(self, text: str, config: CompressionConfig) -> tuple:
        compressed = text
        patterns_matched = 0

        # Apply log templates
        lines = compressed.split('\n')
        compressed_lines = []
        for line in lines:
            new_line = line
            for pattern, template in self.LOG_TEMPLATES:
                match = re.match(pattern, line)
                if match:
                    groups = match.groups()
                    if template is not None:
                        new_line = re.sub(pattern, template, line)
                    else:
                        # Custom handling: strip timestamps, keep meaningful content
                        new_line = self._format_log_line(match, groups)
                    patterns_matched += 1
                    break
            compressed_lines.append(new_line)
        compressed = '\n'.join(compressed_lines)

        # Apply JSON compression
        if config.preserve_json_structure:
            compressed = self._compress_json_blocks(compressed, patterns_matched)

        # Compress table-like structures
        compressed = self._compress_tables(compressed)

        metadata = {"patterns_matched": patterns_matched}
        return compressed, metadata

    def _compress_json_blocks(self, text: str, patterns_matched: int) -> str:
        """Compress JSON blocks within text."""
        lines = text.split('\n')
        result = []
        in_json = False
        json_buffer = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('{') or stripped.startswith('['):
                in_json = True
                json_buffer = [line]
                continue

            if in_json:
                json_buffer.append(line)
                # Simple brace counting to detect end of JSON
                open_braces = sum(l.count('{') + l.count('[') for l in json_buffer)
                close_braces = sum(l.count('}') + l.count(']') for l in json_buffer)
                if open_braces == close_braces and open_braces > 0:
                    json_text = '\n'.join(json_buffer)
                    try:
                        parsed = json.loads(json_text)
                        compact = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
                        result.append(compact)
                        patterns_matched += 1
                    except (json.JSONDecodeError, ValueError):
                        result.extend(json_buffer)
                    in_json = False
                    json_buffer = []
                continue

            result.append(line)

        return '\n'.join(result)

    def _format_log_line(self, match, groups) -> str:
        """Format a matched log line by stripping timestamps and keeping meaningful content."""
        line = match.group(0)
        # Determine format by number of groups
        if len(groups) == 2:
            # [TIMESTAMP] LEVEL - message  ->  LEVEL: message
            timestamp, level = groups
            rest = line[match.end():]
            return f"{level}:{rest}" if rest else f"{level}"
        elif len(groups) == 3:
            # Standard log: [TS] LEVEL - msg  ->  LEVEL: msg
            timestamp, level, message = groups
            return f"{level}: {message}"
        elif len(groups) == 4:
            # Syslog: date host service: msg  ->  service: msg
            date, host, service, message = groups
            return f"{service}: {message}"
        elif len(groups) == 5:
            # Java-style: [TS] LEVEL [thread] pkg - msg  ->  LEVEL [thread]: msg
            timestamp, level, thread, package, message = groups
            return f"{level} [{thread}]: {message}"
        return line

    def _compress_tables(self, text: str) -> str:
        """Compress markdown-style tables."""
        lines = text.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detect table separator
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                # This is a table separator, skip it
                i += 1
                continue
            result.append(line)
            i += 1
        return '\n'.join(result)
