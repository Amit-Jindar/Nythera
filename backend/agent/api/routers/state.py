from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2] / "data/dashboards/final/state"
VALID_PANELS = {f"PANEL_{i}" for i in range(1, 7)}

# -------------------------------------------------
# NO-CACHE HELPER
# -------------------------------------------------

def nocache(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"


# -------------------------------------------------
# LOAD STATE FILE
# -------------------------------------------------

def load_state(state: str) -> dict:
    """
    Load state JSON exactly like district loader.
    """
    file_path = BASE_DIR / f"{state.replace(' ', '_')}.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"State data not found for '{state}'"
        )

    return json.loads(file_path.read_text("utf-8"))


# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@router.get("/{state}")
def state_all(state: str, response: Response):
    """
    FULL STATE DASHBOARD
    (Same contract as district_all)
    """
    nocache(response)

    try:
        data = load_state(state)
        return {
            "scope": "state",
            "state": state,
            "panels": {
                k: v for k, v in data.items() if k in VALID_PANELS
            },
            "meta": data.get("meta"),
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{state}/{panel}")
def state_panel(state: str, panel: str, response: Response):
    """
    SINGLE STATE PANEL
    (Same contract style as district_panel)
    """
    nocache(response)

    panel = panel.upper()
    if panel not in VALID_PANELS:
        raise HTTPException(status_code=404, detail="Invalid panel")

    try:
        data = load_state(state)

        if panel not in data:
            raise HTTPException(status_code=404, detail="Panel not found")

        return {
            "scope": "state",
            "state": state,
            "panel": panel,
            "data": data[panel],
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
