from typing import Annotated

from fastapi import Depends

from schemas.short_url import ShortUrl
from fastapi import APIRouter

from .dependencies import (
    prefetch_short_urls,
)
from .crud import SHORT_URLS

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/short-urls/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


@router.get(
    "/short-urls/{slug}/",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return url
