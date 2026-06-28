import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from core.orchestrator import CampaignOrchestrator

orchestrator = CampaignOrchestrator()
event_data = {
    "event_name": "SANGAM 2.0 Campaign Launch",
    "date": "TBD",
    "territory": "TBD",
    "location": "TBD",
    "objective": "highlighting the synergistic benefits of Seminis Adhik hybrid tomatoes and Camalus® insecticide.",
    "product_focus": "Seminis Adhik & Camalus®"
}
platforms = ["Internal WhatsApp", "Farmer WhatsApp"]
languages = ["English"]

res = orchestrator.generate_campaign(event_data, platforms, languages)
print("GENERATED CAMPAIGN:")
print(json.dumps(res, indent=2))
