import pandas as pd

def parse_csv_events(df: pd.DataFrame) -> list[dict]:
    """
    Parses the event DataFrame into a structured list of dictionaries.
    Handles legacy formats and JSON-encoded location fields.
    """
    events = []
    for _, row in df.iterrows():
        event_name = row.get("Title", "Unknown Event")
        date = row.get("Event Date", "Unknown Date")
        territory = row.get("Territory", "Unknown Territory")
        location_raw = row.get("Event Location", "Unknown Location")
        
        if pd.isna(location_raw):
            location = "Unknown Location"
        elif "DisplayName" in str(location_raw):
            try:
                import json
                loc_dict = json.loads(location_raw)
                location = loc_dict.get("DisplayName", "Unknown Location")
            except:
                location = str(location_raw)[:30]
        else:
            location = str(location_raw)

        events.append({
            "event_name": event_name,
            "date": date,
            "territory": territory,
            "location": location,
            "objective": row.get("Objective / Purpose", ""),
            "estimated_farmers": row.get("Estimated Farmers", 0),
            "product_focus": row.get("Product /Combo Focus", ""),
            "participants": row.get("Participants from Commercial(CP + Seminis)", ""),
            "group_lob": row.get("Group / LOB", "")
        })
    return events
