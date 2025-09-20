from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.short_urls.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # Действия до запуска приложения.
    storage.init_storage_from_state()
    # Ставим функцию на паузу на время
    # работы приложения.
    yield
    # Действия перед завершением работы
    # приложения.
