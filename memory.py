import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
load_dotenv()
BANK = os.getenv("HINDSIGHT_BANK", "incident-responder")

def _c():
    return Hindsight(base_url=os.environ["HINDSIGHT_BASE_URL"], api_key=os.getenv("HINDSIGHT_API_KEY"))

def retain(i: dict) -> bool:
    """Store one incident as a sentence. Returns False on any failure."""
    try:
        _c().retain(bank_id=BANK, content=f"{i['service']} had {i['symptom']}. Root cause: {i['root_cause']}. Fix '{i['fix']}' {'worked' if i['resolved'] else 'did not work'}.")
        return True
    except Exception:
        return False

def recall(symptom: str) -> list[str]:
    """Recall past incident text for a symptom. Empty list on failure."""
    try:
        return [r.text for r in _c().recall(bank_id=BANK, query=f"incidents with {symptom}").results[:5]]
    except Exception:
        return []
