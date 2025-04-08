import logging

from lib.models.constants.const_config import ConfigKey
from lib.util.encoding_util import decrypt_cipher_text

MARIADB_CONNECTION_STRING = (
    'mysql+pymysql://{username}:{password}@{hostname}:{port}/{dbname}'
)

MARIADB_CONNECTION_KEYS = [ConfigKey.KEY_USERNAME, ConfigKey.KEY_PASSWORD, ConfigKey.KEY_HOSTNAME,
                           ConfigKey.KEY_PORT, ConfigKey.KEY_DBNAME]

logging.basicConfig(level=logging.DEBUG)


def get_mariadb_connect_info(yaml_loader, section):
    config = yaml_loader.load_config()

    if section not in config:
        logging.error(f"cannot find section : {section}")
        return None

    hostname = config[section].get(ConfigKey.KEY_HOSTNAME.key, None)
    port = config[section].get(ConfigKey.KEY_PORT.key, None)
    dbname = config[section].get(ConfigKey.KEY_DBNAME.key, None)
    username = config[section].get(ConfigKey.KEY_USERNAME.key, None)
    password = config[section].get(ConfigKey.KEY_PASSWORD.key, None)

    return MariadbConnectInfo(hostname, port, dbname, username, password)


class MariadbConnectInfo:
    def __init__(self, hostname, port, dbname, username, password):
        self.hostname = hostname
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password

    def is_valid(self):
        return all(
            attr is not None
            for attr in [
                self.hostname,
                self.port,
                self.dbname,
                self.username,
                self.password
            ]
        )

    def get_connect_string(self):
        return MARIADB_CONNECTION_STRING.format(
            username=self.username,
            password=decrypt_cipher_text(self.password),
            hostname=self.hostname,
            port=self.port,
            dbname=self.dbname,
        )

    def get_value_by_config_key(self, config_key: ConfigKey):
        if config_key == ConfigKey.KEY_HOSTNAME:
            return self.hostname
        elif config_key == ConfigKey.KEY_PORT:
            return self.port
        elif config_key == ConfigKey.KEY_DBNAME:
            return self.dbname
        elif config_key == ConfigKey.KEY_USERNAME:
            return self.username
        elif config_key == ConfigKey.KEY_PASSWORD:
            return self.password
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")

    def set_value_by_config_key(self, config_key: ConfigKey, value):
        if config_key == ConfigKey.KEY_HOSTNAME:
            self.hostname = value
        elif config_key == ConfigKey.KEY_PORT:
            self.port = value
        elif config_key == ConfigKey.KEY_DBNAME:
            self.dbname = value
        elif config_key == ConfigKey.KEY_USERNAME:
            self.username = value
        elif config_key == ConfigKey.KEY_PASSWORD:
            self.password = value
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")
