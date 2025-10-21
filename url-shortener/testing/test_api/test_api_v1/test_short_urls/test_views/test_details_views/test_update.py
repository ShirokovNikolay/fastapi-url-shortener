from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from pydantic import AnyHttpUrl
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import DESCRIPTION_MAX_LENGTH, ShortUrl, ShortUrlUpdate
from testing.conftest import create_short_url_random_slug


class TestUpdate:
    @pytest.fixture
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        description, target_url = request.param
        short_url = create_short_url_random_slug(
            description=description,
            target_url=target_url,
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description, new_target_url",
        [
            pytest.param(
                ("some description", "https://example.com"),
                "some description",
                "https:google.com",
                id="same-description-and-new-target-url",
            ),
            pytest.param(
                ("old description", "https://example.com"),
                "new description",
                "https://leetcode.com",
                id="new-description-and-new-target-url",
            ),
            pytest.param(
                ("basic description", "https://example.com"),
                "",
                "https://yandex.ru",
                id="empty-description-and-new-target-url",
            ),
            pytest.param(
                ("the description", "https://yandex.ru"),
                "a" * DESCRIPTION_MAX_LENGTH,
                "https://yandex.ru",
                id="max-description-and-same-target-url",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_movie_details(
        self,
        short_url: ShortUrl,
        new_description: str,
        new_target_url: AnyHttpUrl,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_short_url_details",
            slug=short_url.slug,
        )
        short_url_update = ShortUrlUpdate(
            description=new_description,
            target_url=new_target_url,
        )
        response = auth_client.put(
            url=url,
            json=short_url_update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(slug=short_url.slug)
        assert short_url_db

        new_data = ShortUrlUpdate(**short_url_db.model_dump(mode="json"))
        assert new_data == short_url_update
