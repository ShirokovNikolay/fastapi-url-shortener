from typing import Annotated

from annotated_types import Len

from fastapi import (
    APIRouter,
    Depends,
    status,
    Form,
)
from pydantic import AnyHttpUrl

from schemas.short_url import ShortUrl

from .dependencies import (
    prefetch_short_urls,
)
from .crud import SHORT_URLS

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    target_url: Annotated[AnyHttpUrl, Form()],
    slug: Annotated[
        str,
        Form(),
        Len(min_length=3, max_length=10),
    ],
):
    return ShortUrl(
        slug=slug,
        target_url=target_url,
    )


@router.get(
    "/{slug}/",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return url
