# Troubleshooting

## API Key Errors
If you see a `401 UNAUTHENTICATED` error, verify that `.env` contains a valid `GEMINI_API_KEY`.

## Quota Errors
If you see an "AI Service Experiencing High Demand" error (HTTP 429), the Free Tier 20 RPM limit has been exceeded. Wait 60 seconds and click Generate again.
