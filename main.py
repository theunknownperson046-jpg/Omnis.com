from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.responses import Response
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(
    title="FastAPI Learning",
    description="FastAPI application with Jinja2",
    version="1.0.0"
)

SESSION_SECRET = os.getenv("SESSION_SECRET","ti9AOpCELi-ac82-YhWynwj7I16bgC6YqpAfQ3K4TWYKywmde2SdD5JWFq4QrSxS")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="fastapi_session",
    max_age=3600,
    same_site="lax",
    https_only=os.getenv("ENVIRONMENT") == "production"
)

uid = {
    "admin": "password"
}

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
VERIFY = os.getenv("VERIFY")

balance = 1000.0  

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.head("/")
async def home_head():
    return Response(status_code=200)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
        if request.session.get("VERIFY"):
            return RedirectResponse(
                url="/dashboard",
                status_code=303
            )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"title": "FastAPI Application"}
        )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not request.session.get("VERIFY"):
        return RedirectResponse(
            url="/",
            status_code=303
        )
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"verified": True, "title": "FastAPI Application", "login": USERNAME, "Balance": "$" + str(balance)}
    )
'''
@app.post("/Transaction")
async def transaction(request: Request, amount: float = Form(...)):
    global balance
    balance += amount
    pass
'''
@app.post("/")
async def login_user(request: Request, login: str = Form(...), password: str = Form(...)):
    if login in uid and password == uid[login]:
        request.session["VERIFY"] = True
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"title": "FastAPI Application", "error": "Invalid username or password!"}
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

