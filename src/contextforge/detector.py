"""
Content type detection utilities.
"""

import re
from typing import Optional, Tuple
from .models import ContentType


class ContentDetector:
    """Detects the type of content for optimal compression strategy selection."""

    # Patterns for content type detection
    PATTERNS = {
        ContentType.LOG: [
            r'^\[\d{4}-\d{2}-\d{2}',
            r'^\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}',
            r'^(?:DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL|TRACE)\s',
            r'^\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',
            r'^\[(?:DEBUG|INFO|WARN|ERROR|FATAL)\]',
            r'^\d{2}:\d{2}:\d{2}\.\d{3}\s+(?:DEBUG|INFO|WARN|ERROR)',
            r'^\s*(?:DEBUG|INFO|WARN|ERROR|FATAL)\s*:',
            r'^\w{3}\s+\d{1,2}\s+\d{4}\s+\d{2}:\d{2}:\d{2}',
        ],
        ContentType.JSON: [
            r'^\s*\{',
            r'^\s*\[',
        ],
        ContentType.XML: [
            r'^\s*<\?xml',
            r'^\s*<[a-zA-Z][^>]*>',
        ],
        ContentType.HTML: [
            r'<(!DOCTYPE|html|head|body|div|span|p|a|table|form)\b',
            r'</(html|head|body|div|span|p|a|table|form)>',
        ],
        ContentType.MARKDOWN: [
            r'^#{1,6}\s+',
            r'^\s*[-*+]\s+',
            r'^\s*\d+\.\s+',
            r'\[.*?\]\(.*?\)',
            r'^\s*>\s+',
            r'^```',
            r'\*\*.*?\*\*',
        ],
        ContentType.CODE: [
            r'^(?:import|from|def|class|function|const|let|var|public|private|protected)\s',
            r'^(?:if|else|for|while|switch|try|catch|finally)\s*[\(:]',
            r'^\s*(?:return|yield|await|async)\s',
            r'#[!/]usr/bin/env',
        ],
        ContentType.CSV: [
            r'^[^,\n]+(,[^,\n]+)+$',
        ],
        ContentType.CONVERSATION: [
            r'^(?:Human|Assistant|User|System|AI|Bot)\s*:',
            r'^\[(?:HUMAN|ASSISTANT|USER|SYSTEM|AI|BOT)\]',
        ],
        ContentType.TOOL_OUTPUT: [
            r'^(?:Result|Output|Response|Return|Status)\s*:',
            r'^\{[\s\S]*"result"[\s\S]*\}',
            r'^\{[\s\S]*"output"[\s\S]*\}',
        ],
    }

    @classmethod
    def detect(cls, text: str) -> ContentType:
        """Detect the content type of the given text."""
        if not text or not text.strip():
            return ContentType.TEXT

        lines = text.strip().split('\n')
        sample_lines = lines[:min(20, len(lines))]
        scores = {}

        for content_type, patterns in cls.PATTERNS.items():
            score = 0
            for line in sample_lines:
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE | re.MULTILINE):
                        score += 1
                        break
            if score > 0:
                scores[content_type] = score

        if not scores:
            return ContentType.TEXT

        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]

        # Require at least 2 matching lines for non-text types
        if best_score < 2 and best_type != ContentType.TEXT:
            stripped = text.strip()
            if stripped.startswith('{') or stripped.startswith('['):
                try:
                    import json
                    json.loads(stripped)
                    return ContentType.JSON
                except (json.JSONDecodeError, ValueError):
                    pass
            return ContentType.TEXT

        return best_type

    @classmethod
    def detect_with_confidence(cls, text: str) -> Tuple[ContentType, float]:
        """Detect content type with confidence score."""
        if not text or not text.strip():
            return ContentType.TEXT, 0.0

        lines = text.strip().split('\n')
        sample_lines = lines[:min(20, len(lines))]
        scores = {}

        for content_type, patterns in cls.PATTERNS.items():
            score = 0
            for line in sample_lines:
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE | re.MULTILINE):
                        score += 1
                        break
            if score > 0:
                scores[content_type] = score / len(sample_lines)

        if not scores:
            return ContentType.TEXT, 0.0

        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        return best_type, round(confidence, 3)
