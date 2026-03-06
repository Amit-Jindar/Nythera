from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2] / "data/dashboards/final/tehsil"
VALID_PANELS = {f"PANEL_{i}" for i in range(1, 7)}

# -------------------------------------------------
# NO-CACHE (REFRESH BUG FIX)
# -------------------------------------------------

def nocache(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"


# -------------------------------------------------
# DISTRICT DIR RESOLVER
# -------------------------------------------------

def resolve_district_dir(district: str) -> Path | None:
    normalized = district.strip()

    candidates = {
        normalized,
        normalized.replace(" ", "_"),
        normalized.replace("_", " "),
        normalized.replace(" ", "").replace("_", ""),
    }

    for d in BASE_DIR.iterdir():
        if not d.is_dir():
            continue

        for c in candidates:
            if d.name.lower() == c.lower():
                return d

    return None


# -------------------------------------------------
# TEHSIL FILE RESOLVER
# -------------------------------------------------

def resolve_tehsil_file(district_dir: Path, tehsil: str) -> Path | None:
    normalized = tehsil.strip()

    candidates = {
        normalized,
        normalized.replace(" ", "_"),
        normalized.replace("_", " "),
        normalized.replace(" ", "").replace("_", ""),
    }

    for f in district_dir.iterdir():
        if not f.is_file() or f.suffix.lower() != ".json":
            continue

        for c in candidates:
            if f.stem.lower() == c.lower():
                return f

    return None


# -------------------------------------------------
# LOAD TEHSIL JSON
# -------------------------------------------------

def load_tehsil(district: str, tehsil: str) -> dict:
    district_dir = resolve_district_dir(district)

    if not district_dir:
        raise FileNotFoundError(
            f"District directory not found for '{district}'"
        )

    tehsil_file = resolve_tehsil_file(district_dir, tehsil)

    if not tehsil_file:
        raise FileNotFoundError(
            f"Tehsil data not found for '{tehsil}' in district '{district}'"
        )

    return json.loads(tehsil_file.read_text("utf-8"))


# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@router.get("/{district}/{tehsil}")
def tehsil_all(district: str, tehsil: str, response: Response):
    nocache(response)

    try:
        data = load_tehsil(district, tehsil)
        return {
            "scope": "tehsil",
            "district": district,
            "tehsil": tehsil,
            "panels": {
                k: v for k, v in data.items() if k in VALID_PANELS
            },
            "meta": data.get("meta"),
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{district}/{tehsil}/{panel}")
def tehsil_panel(
    district: str,
    tehsil: str,
    panel: str,
    response: Response,
):
    nocache(response)

    panel = panel.upper()

    if panel not in VALID_PANELS:
        raise HTTPException(status_code=404, detail="Invalid panel")

    try:
        data = load_tehsil(district, tehsil)

        if panel not in data:
            raise HTTPException(status_code=404, detail="Panel not found")

        return {
            "scope": "tehsil",
            "district": district,
            "tehsil": tehsil,
            "panel": panel,
            "data": data[panel],
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
