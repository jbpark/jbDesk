from enum import Enum


class ConfigKey(Enum):
    KEY_HOSTNAME = ("hostname", False)
    KEY_PORT = ("port", False)
    KEY_SERVICE_NAME = ("service_name", False)
    KEY_DB_FILE = ("db_file", False)
    KEY_DBNAME = ("dbname", False)
    KEY_USERNAME = ("username", False)
    KEY_PASSWORD = ("password", True)

    def __init__(self, key: str, is_secure: bool):
        self._key = key
        self._is_secure = is_secure

    @property
    def key(self) -> str:
        return self._key

    @property
    def is_secure(self) -> bool:
        return self._is_secure
