from pathlib import Path

from fastapi.routing import APIRouter, Request
from fastapi.templating import Jinja2Templates

from microservice.web.api import docs, user, file, admin

pages_router = APIRouter()

APP_ROOT = Path(__file__).parent.parent
templates = Jinja2Templates(directory=APP_ROOT / "templates")


@pages_router.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@pages_router.get("/index")
async def read_index_h(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@pages_router.get("/download")
async def read_download_h(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


@pages_router.get("/admin")
async def read_admin_h(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@pages_router.get("/lk")
async def read_lk_h(request: Request):
    return templates.TemplateResponse("lk.html", {"request": request})


@pages_router.get("/myFiles")
async def readmyFiles_h(request: Request):
    return templates.TemplateResponse("myFiles.html", {"request": request})


@pages_router.get("/registration")
async def read_registration_h(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})