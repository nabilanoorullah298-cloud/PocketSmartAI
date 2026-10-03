from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

import database
from auth_utils import get_current_user, login_redirect
from routes.planner import PLANNERS
from templating import templates

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return login_redirect()
    recent = database.get_history(user["id"], limit=5)
    return templates.TemplateResponse(
        request, "dashboard.html", {"recent": recent, "planners": PLANNERS}
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    user = get_current_user(request)
    if not user:
        return login_redirect()
    items = database.get_history(user["id"])
    return templates.TemplateResponse(
        request, "history.html", {"items": items, "planners": PLANNERS}
    )


@router.get("/history/{item_id}", response_class=HTMLResponse)
def history_detail(request: Request, item_id: int):
    user = get_current_user(request)
    if not user:
        return login_redirect()
    item = database.get_history_item(user["id"], item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return templates.TemplateResponse(
        request, "history_detail.html", {"item": item, "planners": PLANNERS}
    )
