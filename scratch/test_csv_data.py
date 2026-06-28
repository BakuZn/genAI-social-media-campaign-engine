import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from core.orchestrator import CampaignOrchestrator

orchestrator = CampaignOrchestrator()
event_data = {
    "event_name": "Sangam 2.0",
    "date": "6/19/2026 4:52 PM",
    "territory": "Guntur",
    "location": "Bayer House",
    "objective": "farmers meeting",
    "product_focus": "CAMALUS"
}
platforms = ["Internal WhatsApp", "Farmer WhatsApp"]
languages = ["English"]

res = orchestrator.generate_campaign(event_data, platforms, languages)
print("GENERATED CAMPAIGN:")
print(json.dumps(res, indent=2))
