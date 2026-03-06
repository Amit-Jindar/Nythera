from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path("/home/genius/Public/agent/data/dashboards/final/district")
VALID_PANELS = {f"PANEL_{i}" for i in range(1, 7)}

# -------------------------------------------------
# NO-CACHE HELPER (REFRESH BUG FIX)
# -------------------------------------------------

def nocache(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"


# -------------------------------------------------
# FILE RESOLVER (SPACE / UNDERSCORE SAFE)
# -------------------------------------------------

def resolve_district_file(district: str) -> Path | None:
    """
    Resolve district JSON file from human-readable district name.
    Handles spaces, underscores, and casing.
    """

    normalized = district.strip()

    candidates = {
        normalized,
        normalized.replace(" ", "_"),
        normalized.replace("_", " "),
        normalized.replace(" ", "").replace("_", ""),
    }

    for file in BASE_DIR.iterdir():
        if not file.is_file() or file.suffix.lower() != ".json":
            continue

        stem = file.stem  # filename without .json

        for candidate in candidates:
            if stem.lower() == candidate.lower():
                return file

    return None


def load_district(district: str) -> dict:
    file_path = resolve_district_file(district)

    if not file_path:
        raise FileNotFoundError(
            f"District data not found for '{district}'"
        )

    return json.loads(file_path.read_text("utf-8"))


# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@router.get("/{district}")
def district_all(district: str, response: Response):
    nocache(response)

    try:
        data = load_district(district)
        return {
            "scope": "district",
            "district": district,
            "panels": {
                k: v for k, v in data.items() if k in VALID_PANELS
            },
            "meta": data.get("meta"), 
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{district}/{panel}")
def district_panel(district: str, panel: str, response: Response):
    nocache(response)

    panel = panel.upper()

    if panel not in VALID_PANELS:
        raise HTTPException(status_code=404, detail="Invalid panel")

    try:
        data = load_district(district)

        if panel not in data:
            raise HTTPException(status_code=404, detail="Panel not found")

        return {
            "scope": "district",
            "district": district,
            "panel": panel,
            "data": data[panel],
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
