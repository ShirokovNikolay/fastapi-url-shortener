from pydantic import BaseModel

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

import json
from pathlib import Path


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        result = {
            slug: short_url.model_dump_json(indent=2)
            for slug, short_url in self.slug_to_short_url.items()
        }
        path = Path("short_urls.json")
        if not path.exists():
            path.touch()
        with path.open("w") as file:
            json.dump(result, file, indent=2)

    def from_state(self) -> None:
        path = Path("short_urls.json")
        if not path.exists():
            path.touch()
        with path.open("r") as file:
            self.slug_to_short_url = {
                slug: ShortUrl.model_validate_json(short_url)
                for slug, short_url in json.load(file).items()
            }

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug, None)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_in.model_dump())
        self.slug_to_short_url[short_url.slug] = short_url
        self.save_state()
        return short_url

    def delete_by_slug(self, slug) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.save_state()

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)
        self.save_state()

    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url


storage = ShortUrlsStorage()
try:
    storage.from_state()
except json.JSONDecodeError:
    storage.save_state()
