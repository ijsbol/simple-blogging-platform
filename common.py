import glob
import json
import re
from typing import Final, TypedDict

from fastapi.templating import Jinja2Templates
from markdown import markdown


__all__: Final[tuple[str, ...]] = (
    "templates",
    "load_blogs",
)


class BlogAuthor(TypedDict):
    display: str
    avatar: str
    link: str
    colours: list[int]


class BlogMeta(TypedDict):
    authors: list[BlogAuthor]
    tags: list[str]
    title: str
    date: int  # unix timestamp


class Blog(TypedDict):
    html: str
    slug: str
    meta: BlogMeta


templates = Jinja2Templates(directory="templates")


def _find_metadata_end_line(mdx_content: str) -> int:
    lines = mdx_content.splitlines()
    is_metadata = False
    for i, line in enumerate(lines, start=1):
        if line.strip() == "---":
            if is_metadata:
                return i
            is_metadata = True
    raise ValueError("Metadata not present / does not end.")


def _get_author(name: str) -> BlogAuthor:
    with open("blog-authors.json", "r") as f:
        authors = json.loads(f.read())
        return authors[name]


def load_blog(slug: str) -> Blog:
    file_path = f"blogs/{slug}.mdx"
    with open(file_path, "r") as f:
        content = f.read()
    file_lines = content.split("\n")
    end_metadata = _find_metadata_end_line(content)
    blog_content = '\n'.join(file_lines[end_metadata:])
    metadata_match = re.search(r"^---(.*?)---", content, re.DOTALL)
    if not metadata_match:
        raise ValueError("Meta data not present.")

    metadata = metadata_match.group(1).strip()
    metadata_dict = {}
    for line in metadata.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):  # List
                value = value.strip("[]").split(",")
            elif value.startswith('"') and value.endswith('"'):  # String
                value = value[1:-1]
            metadata_dict[key] = value

    authors = [_get_author(a) for a in metadata_dict['authors']]
    date = int(metadata_dict['date'])
    del metadata_dict['authors']
    del metadata_dict['date']
    return Blog(
        html=markdown(blog_content),
        slug=_clean_slug(slug),
        meta=BlogMeta(
            date=date,
            authors=authors,
            **metadata_dict,
        ),
    )


def _clean_slug(slug: str) -> str:
    return slug.removeprefix("private.").removeprefix("blog.")


def load_blogs(*, include_private: bool = False) -> dict[str, Blog]:
    blogs = glob.glob("blogs/blog.*.mdx")
    blogs.extend(glob.glob("blogs/private.*.mdx"))
    print(blogs)
    blog_slugs: list[str] = [
        name.split("/")[1].removesuffix(".mdx")
        for name in blogs
    ]
    return {
        _clean_slug(slug): load_blog(slug)
        for slug in blog_slugs
        if ((slug.startswith("private.") and include_private) or slug.startswith("blog."))
    }
