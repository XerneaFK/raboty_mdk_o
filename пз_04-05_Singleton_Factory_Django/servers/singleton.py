
class AccessManager:
    """Singleton: единый менеджер доступа к базе данных."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.access_log = []

        return cls._instance

    def record_access(self, request_info: str) -> None:
        self.access_log.append(request_info)

    def get_access_log(self) -> list:
        return self.access_log
