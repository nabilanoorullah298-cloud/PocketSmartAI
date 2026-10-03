from fastapi.responses import RedirectResponse

import database
import security


def get_current_user(request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = security.decode_token(token)
    if not payload:
        return None
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError):
        return None
    return database.get_user_by_id(user_id)


def login_redirect():
    return RedirectResponse("/login", status_code=303)
