import logging

import cx_Oracle

from lib.models.constants.config_key import ConfigKey
from lib.util.encoding_util import decrypt_cipher_text

ORACLE_CONNECT_STRING = (
        'oracle+cx_oracle://{user_name}:{password}@' +
        cx_Oracle.makedsn('{host_name}', '{port}', service_name='{service_name}')
)

ORACLE_CONNECT_KEYS = [ConfigKey.KEY_USER_NAME, ConfigKey.KEY_PASSWORD, ConfigKey.KEY_HOST_NAME,
                       ConfigKey.KEY_PORT, ConfigKey.KEY_SERVICE_NAME]

logging.basicConfig(level=logging.DEBUG)


def get_oracle_connect_info(yaml_loader, section):
    config = yaml_loader.load_config()

    if section not in config:
        logging.error(f"cannot find section : {section}")
        return None

    host_name = config[section].get(ConfigKey.KEY_HOST_NAME.key, None)
    port = config[section].get(ConfigKey.KEY_PORT.key, None)
    service_name = config[section].get(ConfigKey.KEY_SERVICE_NAME.key, None)
    user_name = config[section].get(ConfigKey.KEY_USER_NAME.key, None)
    password = config[section].get(ConfigKey.KEY_PASSWORD.key, None)

    return OracleConnectInfo(host_name, port, service_name, user_name, password)


class OracleConnectInfo:
    def __init__(self, host_name, port, service_name, user_name, password):
        self.host_name = host_name
        self.port = port
        self.service_name = service_name
        self.user_name = user_name
        self.password = password

    def is_valid(self):
        return all(
            attr is not None
            for attr in [
                self.host_name,
                self.port,
                self.service_name,
                self.user_name,
                self.password
            ]
        )

    def get_connect_string(self):
        return ORACLE_CONNECT_STRING.format(
            user_name=self.user_name,
            password=decrypt_cipher_text(self.password),
            host_name=self.host_name,
            port=self.port,
            service_name=self.service_name,
        )

    def get_value_by_config_key(self, config_key: ConfigKey):
        if config_key == ConfigKey.KEY_HOST_NAME:
            return self.host_name
        elif config_key == ConfigKey.KEY_PORT:
            return self.port
        elif config_key == ConfigKey.KEY_SERVICE_NAME:
            return self.service_name
        elif config_key == ConfigKey.KEY_USER_NAME:
            return self.user_name
        elif config_key == ConfigKey.KEY_PASSWORD:
            return self.password
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")

    def set_value_by_config_key(self, config_key: ConfigKey, value):
        if config_key == ConfigKey.KEY_HOST_NAME:
            self.host_name = value
        elif config_key == ConfigKey.KEY_PORT:
            self.port = value
        elif config_key == ConfigKey.KEY_SERVICE_NAME:
            self.service_name = value
        elif config_key == ConfigKey.KEY_USER_NAME:
            self.user_name = value
        elif config_key == ConfigKey.KEY_PASSWORD:
            self.password = value
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")
