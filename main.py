from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import Response

app = FastAPI(
    title="FastAPI Learning",
    description="FastAPI application with Jinja2",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.head("/")
async def home_head():
    return Response(status_code=200)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FastAPI Application"}
    )

@app.get("/api/status")
async def status():
    return {
        "status": "success",
        "message": "FastAPI is running successfully!"
    }

@app.exception_handler(404)
async def not_found_handler(
    request: Request,
    exc
):
    return templates.TemplateResponse(
        request=request,
        name="not-found.html",
        context={"title": "404 - Page Not Found"},
        status_code=404
    )

