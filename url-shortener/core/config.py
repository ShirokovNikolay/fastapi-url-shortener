import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "gQ3ISZI1o_dZ44x8CyBCng",
        "tXsXDqR4NMAmGgyGz3ih5Q",
    }
)

USERS_DB: dict[str, str] = {
    # username: password
    "Nikolay": "qwerty567",
    "Ivan": "password",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
