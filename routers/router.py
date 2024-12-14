from typing import Final

from fastapi import APIRouter
from fastapi.requests import Request
from starlette.templating import _TemplateResponse

from common import load_blogs, templates


__all__: Final[tuple[str, ...]] = (
    "router",
)


router = APIRouter()


@router.get("/")
async def home(request: Request) -> _TemplateResponse:
    blogs = load_blogs()
    return templates.TemplateResponse( # pyright: ignore[reportUnknownMemberType]
        name="home.jinja",
        context={
            "request": request,
            "blogs": [v for _, v in blogs.items()],
        },
    )
