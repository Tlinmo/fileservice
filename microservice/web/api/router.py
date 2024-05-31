from fastapi.routing import APIRouter

from microservice.web.api import docs, user

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(user.router, prefix="/user", tags=["user"])
