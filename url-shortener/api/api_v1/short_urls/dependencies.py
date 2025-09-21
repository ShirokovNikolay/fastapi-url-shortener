import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Header,
    status,
)

from schemas.short_url import ShortUrl
from .crud import storage
from core import config

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_short_urls(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
) -> None:
    # Выполняется код до входа внутрь view функции.
    yield
    # Выполняется код после выхода из view функции.
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def api_token_required(
    api_token: Annotated[
        str,
        Header(alias="x-auth-token"),
    ],
) -> None:
    if api_token not in config.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )
