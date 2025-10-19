from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import AnyHttpUrl, BaseModel

DESCRIPTION_MAX_LENGTH = 200

DescriptionString = Annotated[
    str,
    MaxLen(DESCRIPTION_MAX_LENGTH),
]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString


class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания сокращённой ссылки.
    """

    # noinspection PyTypeHints
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
    description: DescriptionString = ""


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления информации о сокращённой ссылке.
    """


class ShortUrlPartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации
    о сокращённой ссылке.
    """

    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None


class ShortUrlRead(ShortUrlBase):
    """
    Модель для чтения данных по короткой ссылке.
    """

    slug: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращённой ссылки.
    """

    slug: str
