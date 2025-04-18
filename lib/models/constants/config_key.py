from enum import Enum

# api key
API_KEY = "change_api_key"

LDAP_KEY = 'q-HM05uN6l1kGNq_4l85T43j2jAQFrNkqF4rZIy3kw8='

class ConfigKey(Enum):
    KEY_HOST_NAME = ("host_name", False)
    KEY_PORT = ("port", False)
    KEY_SERVICE_NAME = ("service_name", False)
    KEY_DB_FILE = ("db_file", False)
    KEY_DB_NAME = ("db_name", False)
    KEY_USER_NAME = ("user_name", False)
    KEY_PASSWORD = ("password", True)
    KEY_PRIVATE_IP = ("private_ip", False)
    KEY_PUBLIC_IP = ("public_ip", False)
    KEY_GATEWAY = ("gateway", False)
    KEY_ENV = ("env", False)
    KEY_PROJECT = ("project", False)
    KEY_GROUP = ("group", False)

    def __init__(self, key: str, is_secure: bool):
        self._key = key
        self._is_secure = is_secure

    @property
    def key(self) -> str:
        return self._key

    @property
    def is_secure(self) -> bool:
        return self._is_secure
