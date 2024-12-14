from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

from routers.blog.router import router as blog_router
from routers.router import router as home_router


__all__: Final[tuple[str, ...]] = ()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield


app = FastAPI(
    reload=True,
    debug=True,
    lifespan=app_lifespan,
    docs_url=None,
    redoc_url=None,
    terms_of_service=None,
)


app.mount("/static", StaticFiles(directory="static"), name="static")


routers: list[tuple[APIRouter, str]] = [
    (blog_router, "/blog"),
    (home_router, ""),
]


for router, prefix in routers:
    app.include_router(router, prefix=prefix)
