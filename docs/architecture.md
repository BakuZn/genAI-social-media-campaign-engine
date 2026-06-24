# Bayer GenAI Social Media Campaign Engine - Architecture

## Overview
The platform uses a two-stage transcreation workflow powered by Google Gemini.
1. Master English copy generation from CSV data and OCR.
2. High-fidelity transcreation into regional languages using structured JSON constraints.

## Tech Stack
* Python 3.10+
* Streamlit (Frontend)
* Google GenAI SDK (LLM)
* Pydantic (Data validation - planned)
