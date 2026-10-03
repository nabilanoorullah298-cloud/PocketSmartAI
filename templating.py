import markdown
from fastapi.templating import Jinja2Templates

from auth_utils import get_current_user


def add_user(request):
    return {"user": get_current_user(request)}


templates = Jinja2Templates(directory="templates", context_processors=[add_user])
templates.env.filters["md"] = lambda text: markdown.markdown(text or "", extensions=["tables"])
