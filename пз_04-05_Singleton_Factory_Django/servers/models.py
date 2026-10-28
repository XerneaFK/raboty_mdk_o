
class AccessRequest:
    """Базовый класс запроса доступа к БД."""

    def __init__(self, username: str, database: str):
        self.username = username
        self.database = database

    def get_info(self) -> str:
        raise NotImplementedError(
            "Метод get_info должен быть переопределён"
        )


class ReadRequest(AccessRequest):
    def get_info(self) -> str:
        return (
            f"Read: пользователь {self.username} "
            f"запрашивает чтение БД {self.database}"
        )


class WriteRequest(AccessRequest):
    def get_info(self) -> str:
        return (
            f"Write: пользователь {self.username} "
            f"запрашивает изменение БД {self.database}"
        )


class AdminRequest(AccessRequest):
    def get_info(self) -> str:
        return (
            f"Admin: пользователь {self.username} "
            f"запрашивает административный доступ к БД "
            f"{self.database}"
        )


class AccessRequestFactory:
    """Фабрика запросов на доступ к базе данных."""

    _registry = {
        "read": ReadRequest,
        "write": WriteRequest,
        "admin": AdminRequest,
    }

    @classmethod
    def create(cls, access_type: str, username: str, database: str):
        request_class = cls._registry.get(access_type.lower())

        if request_class is None:
            raise ValueError(
                f"Неизвестный тип доступа: {access_type}"
            )

        return request_class(username, database)
