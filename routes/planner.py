from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse

import database
from auth_utils import get_current_user, login_redirect
from services.gemini_service import get_recommendations
from templating import templates

router = APIRouter()

ALLOWED_IMAGES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

PLANNERS = {
    "home": {
        "title": "Home Interior Budget Planner",
        "hint": "e.g. 4 ceiling fans, 6 lights, 1 dining table",
    },
    "party": {
        "title": "Party Budget Planner",
        "hint": "e.g. birthday for 30 guests: decoration, cake, snacks, music",
    },
    "jewelry": {
        "title": "Jewelry Budget Planner",
        "hint": "e.g. gold necklace set and earrings for a wedding",
    },
}


def render(request, kind, budget="", details="", preferences="", result=None, error=None):
    return templates.TemplateResponse(
        request,
        "planner.html",
        {
            "kind": kind,
            "planner": PLANNERS[kind],
            "budget": budget,
            "details": details,
            "preferences": preferences,
            "result": result,
            "error": error,
        },
    )


@router.get("/planner/{kind}", response_class=HTMLResponse)
def planner_page(request: Request, kind: str):
    if kind not in PLANNERS:
        raise HTTPException(status_code=404, detail="Planner not found")
    if not get_current_user(request):
        return login_redirect()
    return render(request, kind)


@router.post("/planner/{kind}", response_class=HTMLResponse)
def planner_submit(
    request: Request,
    kind: str,
    budget: int = Form(...),
    details: str = Form(...),
    preferences: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    if kind not in PLANNERS:
        raise HTTPException(status_code=404, detail="Planner not found")
    user = get_current_user(request)
    if not user:
        return login_redirect()

    image_bytes = None
    mime_type = None
    if kind == "jewelry" and image is not None and image.filename:
        if image.content_type not in ALLOWED_IMAGES:
            return render(
                request, kind, budget, details, preferences,
                error="Please upload a JPG, PNG or WEBP image.",
            )
        image_bytes = image.file.read(MAX_IMAGE_BYTES + 1)
        if len(image_bytes) > MAX_IMAGE_BYTES:
            return render(
                request, kind, budget, details, preferences,
                error="Image is too large. Please use one under 5 MB.",
            )
        mime_type = image.content_type

    text = get_recommendations(kind, budget, details, preferences, image_bytes, mime_type)
    if text:
        saved_details = details + (" (with reference image)" if image_bytes else "")
        database.add_history(user["id"], kind, budget, saved_details, preferences, text)
        return render(request, kind, budget, details, preferences, result=text)
    error = "Google's server is busy right now. Please try again in a minute."
    return render(request, kind, budget, details, preferences, error=error)
