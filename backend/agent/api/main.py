from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.state import router as state_router
from routers.district import router as district_router
from routers.tehsil import router as tehsil_router

# -----------------------------
# CREATE APP FIRST (IMPORTANT)
# -----------------------------
app = FastAPI(
    title="National Situational Intelligence API",
    version="1.0.0",
    description="State, District, and Tehsil intelligence (read-only)"
)

# -----------------------------
# CORS (frontend support)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(state_router, prefix="/api/state", tags=["state"])
app.include_router(district_router, prefix="/api/district", tags=["district"])
app.include_router(tehsil_router, prefix="/api/tehsil", tags=["tehsil"])

# -----------------------------
# HEALTH
# -----------------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "National Situational Intelligence API"
    }
