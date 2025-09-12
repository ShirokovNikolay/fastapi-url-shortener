from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from schemas.short_url import ShortUrl

from api.api_v1.short_urls.dependencies import (
    prefetch_short_urls,
)
from api.api_v1.short_urls.crud import storage

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return url


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
) -> None:
    storage.delete(short_url=url)
