from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:
    a = 1
    b = 2
    c = add(a, b)
    print("Type c:", type(c))
    # reveal_type(c)
    print(redis.ping())
    redis.set("name", "Nikolay")
    redis.set("foo", "bar")
    redis.set("number", "42")
    print(
        [
            redis.get("foo"),
            redis.get("spam"),
        ],
    )
    redis.delete("name")
    print(redis.get("name"))


if __name__ == "__main__":
    main()
