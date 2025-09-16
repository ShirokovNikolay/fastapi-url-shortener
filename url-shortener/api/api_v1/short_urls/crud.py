import json

from pydantic import BaseModel, AnyHttpUrl
from pydantic_core import from_json

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        result = {
            slug: short_url.model_dump_json(indent=2)
            for slug, short_url in self.slug_to_short_url.items()
        }
        with open("short_urls.json", "w") as file:
            json.dump(result, file, indent=2)

    def from_state(self) -> None:
        with open("short_urls.json", "r") as file:
            self.slug_to_short_url = {
                slug: from_json(short_url)
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
