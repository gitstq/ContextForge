"""
ContextForge CLI - Command-line interface for the compression engine.
"""

import argparse
import json
import sys
import os
from typing import Optional


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="contextforge",
        description="🦞 ContextForge - Lightweight LLM Context Intelligent Compression Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compress a log file
  contextforge compress app.log --type log --level aggressive

  # Compress stdin
  cat output.json | contextforge compress - --type json

  # Detect content type
  contextforge detect myfile.txt

  # Estimate tokens
  contextforge tokens myfile.txt

  # Show compression stats as JSON
  contextforge compress data.json --json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Compress command
    compress_parser = subparsers.add_parser(
        "compress",
        help="Compress text or file content",
    )
    compress_parser.add_argument(
        "input",
        help="Input file path or '-' for stdin",
    )
    compress_parser.add_argument(
        "-t", "--type",
        choices=["auto", "log", "code", "json", "xml", "markdown", "text",
                 "tool_output", "rag_chunks", "conversation", "html", "csv"],
        default="auto",
        help="Content type (default: auto-detect)",
    )
    compress_parser.add_argument(
        "-l", "--level",
        choices=["light", "balanced", "aggressive"],
        default="balanced",
        help="Compression level (default: balanced)",
    )
    compress_parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)",
    )
    compress_parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON with stats",
    )
    compress_parser.add_argument(
        "--stats",
        action="store_true",
        help="Show compression statistics",
    )
    compress_parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Maximum output token count",
    )
    compress_parser.add_argument(
        "--preserve-lines",
        action="store_true",
        help="Preserve line numbers in output",
    )

    # Detect command
    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect content type of a file",
    )
    detect_parser.add_argument(
        "input",
        help="Input file path or '-' for stdin",
    )

    # Tokens command
    tokens_parser = subparsers.add_parser(
        "tokens",
        help="Estimate token count for a file",
    )
    tokens_parser.add_argument(
        "input",
        help="Input file path or '-' for stdin",
    )

    # Version
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"ContextForge v1.0.0",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Import here to avoid slow startup
    from .compressor import ContextCompressor
    from .models import CompressionConfig, CompressionLevel, ContentType

    # Read input
    if args.input == "-":
        text = sys.stdin.read()
    else:
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()

    if not text.strip():
        print("Error: Input is empty", file=sys.stderr)
        sys.exit(1)

    if args.command == "compress":
        config = CompressionConfig(
            level=CompressionLevel(args.level),
            content_type=ContentType(args.type),
            preserve_line_numbers=args.preserve_lines,
            max_output_tokens=args.max_tokens,
        )
        compressor = ContextCompressor(config)
        result = compressor.compress(text)

        if args.json:
            output = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
        elif args.stats:
            output = _format_stats(result)
        else:
            output = result.compressed_text

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)

    elif args.command == "detect":
        compressor = ContextCompressor()
        detected = compressor.detect_type(text)
        _, confidence = _detect_with_confidence(text)
        print(f"Content Type: {detected.value}")
        print(f"Confidence: {confidence:.1%}")

    elif args.command == "tokens":
        compressor = ContextCompressor()
        tokens = compressor.estimate_tokens(text)
        print(f"Estimated tokens: {tokens}")


def _format_stats(result) -> str:
    """Format compression statistics for display."""
    stats = result.stats
    lines = [
        "╔══════════════════════════════════════════════════╗",
        "║         🦞 ContextForge Compression Stats        ║",
        "╠══════════════════════════════════════════════════╣",
        f"║  Original Length:    {stats.original_length:>10,} chars          ║",
        f"║  Compressed Length:  {stats.compressed_length:>10,} chars          ║",
        f"║  Original Tokens:   {stats.original_tokens:>10,}                ║",
        f"║  Compressed Tokens: {stats.compressed_tokens:>10,}                ║",
        f"║  Tokens Saved:      {stats.tokens_saved:>10,}                ║",
        f"║  Compression Ratio: {stats.compression_ratio:>10.1%}                ║",
        f"║  Processing Time:   {stats.processing_time_ms:>10.2f} ms            ║",
        f"║  Strategies Used:   {', '.join(stats.strategies_used) if stats.strategies_used else 'None':<30}║",
        f"║  Lines Removed:      {stats.lines_removed:>10,}                ║",
        f"║  Patterns Matched:  {stats.patterns_matched:>10,}                ║",
        "╚══════════════════════════════════════════════════╝",
    ]
    return '\n'.join(lines)


def _detect_with_confidence(text: str):
    """Detect content type with confidence."""
    from .detector import ContentDetector
    return ContentDetector.detect_with_confidence(text)


if __name__ == "__main__":
    main()
