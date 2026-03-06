from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health():
    return {
        "status": "ok",
        "service": "National Situational Intelligence API",
        "version": "2.0.0"
    }
