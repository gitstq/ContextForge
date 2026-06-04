"""
Example: Basic usage of ContextForge
"""

from contextforge import ContextCompressor, CompressionLevel

# Example 1: Compress application logs
log_text = """
[2024-06-04 08:15:32.456] DEBUG [main] com.app.Server - Initializing application context
[2024-06-04 08:15:32.789] DEBUG [main] com.app.Config - Loading configuration from /etc/app/config.yml
[2024-06-04 08:15:33.012] INFO  [main] com.app.Database - Connecting to PostgreSQL at db.example.com:5432/app_db
[2024-06-04 08:15:33.456] INFO  [main] com.app.Database - Connection pool initialized (min=5, max=20)
[2024-06-04 08:15:34.012] INFO  [main] com.app.Migration - Applied 3 pending migrations
[2024-06-04 08:15:35.123] INFO  [main] com.app.Server - HTTP server started on 0.0.0.0:8080
[2024-06-04 08:15:35.456] INFO  [main] com.app.Server - Application started in 2.987s
"""

compressor = ContextCompressor()
result = compressor.compress(log_text, level="aggressive")

print("=== Original ===")
print(log_text)
print(f"\n=== Compressed ({result.stats.compression_ratio:.1%} reduction) ===")
print(result.compressed_text)
print(f"\nTokens: {result.stats.original_tokens} → {result.stats.compressed_tokens} (saved {result.stats.tokens_saved})")
print(f"Strategies used: {', '.join(result.stats.strategies_used)}")
