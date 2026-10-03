import sqlite3

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

import config
import database
import security
from templating import templates

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {})


@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    username = username.strip()
    email = email.strip()
    error = None
    if len(username) < 3:
        error = "Username must be at least 3 characters."
    elif "@" not in email:
        error = "Please enter a valid email."
    elif len(password) < 6:
        error = "Password must be at least 6 characters."
    else:
        try:
            database.create_user(username, email, security.hash_password(password))
        except sqlite3.IntegrityError:
            error = "That username or email is already registered."
    if error:
        return templates.TemplateResponse(
            request,
            "register.html",
            {"error": error, "username": username, "email": email},
        )
    return RedirectResponse("/login?registered=1", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    message = "Account created! Please sign in." if request.query_params.get("registered") else None
    return templates.TemplateResponse(request, "login.html", {"message": message})


@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = database.get_user_by_username(username.strip())
    if not user or not security.verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Wrong username or password.", "username": username},
        )
    token = security.create_token(user["id"], user["username"])
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        max_age=config.TOKEN_HOURS * 3600,
    )
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
