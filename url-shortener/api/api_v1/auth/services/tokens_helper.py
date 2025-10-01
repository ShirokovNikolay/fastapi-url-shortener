import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Нужно от обертки:
    - Проверять существование токена
    - Генерировать токен
    - Добавлять токен в хранилище
    - Сгенерировать и сохранить токен в хранилище
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Проверка существования токена в хранилище.

        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Добавление токена в хранилище.

        :param token:
        :return:
        """

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Получение списка токенов из хранилища.
        """
