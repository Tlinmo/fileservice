from fastapi.routing import APIRouter

from microservice.web.api import docs, user, file

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
