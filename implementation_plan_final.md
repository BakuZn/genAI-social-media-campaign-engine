# Final Implementation Plan: Email-Driven Event Architecture

Based on your feedback, here is the finalized execution plan for the Bayer GenAI Social Media Campaign Engine. This architecture is elegant, practical for the MVP, provides a "wow" factor for demos, and solves the Event ID distribution problem gracefully.

## Phase 1: Generating the MS Forms Data (One-off Utility)
To help you build the Microsoft Form quickly, we will create a utility script that reads `crop calendar.xlsx` and extracts the unique lists for State, Region, Territory, Crop, Seed Product, and CP Product. 

- **Deliverable:** A text file (`ms_forms_dropdowns.txt`) containing the exact options. You can copy and paste these lists directly into Microsoft Forms to create your multi-select dropdowns instantly without manual mapping.

## Phase 2: Mocking the Data Backend
We will use a local CSV file to simulate the backend database where MS Form responses are deposited.

- **`data/submissions.csv` [NEW]:** Will contain columns mapping to the MS Form (**Email** / **Requested By**, Event Name, Date, Location, State, Region, Territory, Crop(s), Seed Product(s), CP Product(s), Campaign Objective, Target Audience, Key Messages, and **Status**).
- **Status Tracking:** The `status` column will be `Pending` by default. Once a campaign is generated, it will be marked as `Generated` (or `Failed`) to prevent redundant Gemini calls.
- **Example row:** `daksh@bayer.com,Corn Field Day,2026-08-15,Pune,Maharashtra,... ,Pending`

## Phase 3: Redesigning the Streamlit App (`src/ui/app.py`)
We will completely overhaul the user interface into a clean, 3-step workflow. Everything will remain in Streamlit for the MVP (no saving generated excel files).

### Step 3A: Landing Page (Email Lookup)
- Display a clean landing page with: **Enter Email** (e.g. `daksh@bayer.com`).
- A **[ Load My Events ]** button.
- The app reads `submissions.csv` using the new `src/core/submission_loader.py`.
- Displays a list of the user's events (e.g., "1. Corn Field Day", "2. Cotton Retailer Meet").
- The user selects one event to proceed.

### Step 3B: Generation View (Preview & Selection)
- **Selected Event Preview:** Display all details of the selected event (Name, Date, Location, State, Region, Territory, Crop, Products, Objective, Audience, Key Messages).
- **Status Badge:** Display a badge showing the current status (e.g., `Status: Pending`).
- **Selections:** Present the checkboxes for **Target Languages** and **Platforms**.
- A **[ Generate Campaign ]** button.

### Step 3C: Output & Interactive Action Cards
Once generated (or if already generated), the posts will be displayed as interactive cards.
- **Action Buttons:** At the top of each generated platform/language card (e.g., "LinkedIn - English"), we will place specific action buttons. There are NO expandable raw text sections.
  - **LinkedIn:** `[Copy Post]` | `[Open LinkedIn]`
  - **Facebook:** `[Copy Post]` | `[Open Facebook]`
  - **Instagram:** `[Copy Caption]` | `[Open Instagram]`
  - **WhatsApp:** `[Copy Message]` | `[Open WhatsApp]`
- **WhatsApp "Wow" Feature:** The `[Open WhatsApp]` button will use `urllib.parse` to construct a `https://wa.me/?text=...` URL. When clicked during a demo, it will open WhatsApp Web/App with the generated message already pre-filled!

## Code Changes Overview
1. **`src/scripts/extract_form_options.py` [NEW]:** Python script to parse `crop_calendar.xlsx` and output the text file.
2. **`data/submissions.csv` [NEW]:** The mock database with email routing and status tracking.
3. **`src/core/submission_loader.py` [NEW]:** Cleanly named data loader with `load_submission()` and `row_to_event_data()` functions.
4. **`src/ui/app.py` [MODIFY]:** Total overhaul of the UI to support the Email lookup, Preview, Generate, and interactive Action Cards.
