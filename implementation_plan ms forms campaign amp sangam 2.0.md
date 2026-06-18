# Microsoft Forms Integration Architecture

Yes, it is absolutely possible (and very common in enterprise environments) to decouple the data entry from the application. Instead of users manually typing details into the Streamlit dashboard, marketing managers could simply fill out a standard Microsoft Form.

This document outlines how we would architect that integration.

## Proposed Architecture: The Webhook Approach
The most robust, real-time method to connect Microsoft Forms to a Python application is by using **Microsoft Power Automate** to catch the form submission and send it to our Python backend via a **Webhook**.

### 1. Microsoft Forms & Power Automate (The Trigger)
- **The Form:** You create a Microsoft Form with fields mapping directly to our `AgriculturalEventBrief` schema (Event Name, Location, Date, Crop, Seed Products, etc.).
- **The Automation:** You set up a simple Microsoft Power Automate flow with the trigger: *"When a new response is submitted"*.
- **The Action:** The flow takes the answers and executes an *"HTTP POST"* action, sending the data as a JSON payload to our Python server.

### 2. Python Backend (FastAPI Webhook Receiver)
Currently, our app is purely a Streamlit frontend. To receive data from Microsoft, we need to introduce a lightweight API server (like **FastAPI**).
- We create an endpoint (e.g., `POST /api/webhooks/ms-forms`).
- This endpoint listens 24/7 for the Power Automate payload.
- When a payload arrives, it maps the Microsoft Form fields into our existing Pydantic `AgriculturalEventBrief` model.

### 3. Generation & Storage Pipeline
- Once the webhook is received, the FastAPI server automatically triggers the `CampaignOrchestrator` (the exact same core engine we already built).
- The orchestrator calls Gemini 2.5 Flash, does the batch processing, and generates the English Master and target language translations.
- **Output Routing:** Because this happens in the background (without the user looking at Streamlit), the generated JSON campaign must be saved somewhere. Options include:
  - Saving to a database (SQLite/Postgres).
  - Saving to a local JSON file.
  - Sending it *back* via Power Automate to an Excel sheet, a SharePoint list, or directly emailing it to the person who filled out the form.

---

## Required Codebase Changes

If we proceed with this, here is how the codebase would change:

### [NEW] `src/api/server.py`
A new FastAPI application that exposes the webhook endpoint.

### [MODIFY] `src/core/brief_parser.py`
We will add a helper function `from_ms_form_payload()` to map the weirdly formatted Microsoft JSON into our clean Pydantic model.

### [MODIFY] `requirements.txt`
Add `fastapi` and `uvicorn` (to run the web server).

### [OPTIONAL MODIFY] `src/ui/app.py`
We can convert the Streamlit app from a "Data Entry Form" into a "Campaign Dashboard". Instead of text boxes, it would just show a clean list of all the campaigns that were automatically generated from the Microsoft Forms submissions in the background.

---

## User Review Required

> [!IMPORTANT]
> **Deployment Constraint**
> For Microsoft Power Automate to send data to our Python app, our Python app must be hosted on the public internet (e.g., AWS, Azure, Heroku, or via a tunneling service like Ngrok during local development). It cannot just run locally on your laptop without a tunnel.
>
> **Output Routing Decision**
> If a user fills out a Microsoft Form and the campaign is generated in the background, where do you want the final campaign text to go? 
> 1. Show it in the Streamlit Dashboard?
> 2. Email it back to the submitter?
> 3. Dump it into an Excel Sheet / SharePoint List?

Do you approve of this webhook-based architecture?
