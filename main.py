from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import database
from routes import auth, dashboard, planner
from templating import templates

database.init_db()

app = FastAPI(title="PocketSmart AI")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(planner.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")
