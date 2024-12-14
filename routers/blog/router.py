from typing import Final

from fastapi import APIRouter
from fastapi.requests import Request
from starlette.responses import RedirectResponse, Response

from common import load_blogs, templates


__all__: Final[tuple[str, ...]] = (
    "router",
)


router = APIRouter()


@router.get("/")
async def blog(request: Request) -> RedirectResponse:
    return RedirectResponse(url=request.url_for('home'))


@router.get("/{slug}")
async def blog_slug(request: Request, slug: str) -> Response:
    blogs = load_blogs(include_private=True)
    blog = blogs.get(slug, None)
    if blog is None:
        return RedirectResponse(url=request.url_for('home'))

    return templates.TemplateResponse( # pyright: ignore[reportUnknownMemberType]
        name="blog.jinja",
        context={
            "request": request,
            "blog": blog,
        },
    )
