import logging

from lib.models.constants.const_config import ConfigKey

SQLITE_CONNECTION_STRING = (
    'sqlite:///{db_file}'
)

SQLITE_CONNECTION_KEYS = [ConfigKey.KEY_DB_FILE]

logging.basicConfig(level=logging.DEBUG)


def get_sqlite_connect_info(yaml_loader, section):
    config = yaml_loader.load_config()

    if section not in config:
        logging.error(f"cannot find section : {section}")
        return None

    db_file = config[section].get(ConfigKey.KEY_DB_FILE.key, None)

    return SqliteConnectInfo(db_file)


class SqliteConnectInfo:
    def __init__(self, db_file):
        self.db_file = db_file

    def is_valid(self):
        return all(
            attr is not None
            for attr in [
                self.db_file
            ]
        )

    def get_connect_string(self):
        return SQLITE_CONNECTION_STRING.format(
            db_file=self.db_file,
        )

    def get_value_by_config_key(self, config_key: ConfigKey):
        if config_key == ConfigKey.KEY_DB_FILE:
            return self.db_file
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")

    def set_value_by_config_key(self, config_key: ConfigKey, value):
        if config_key == ConfigKey.KEY_DB_FILE:
            self.db_file = value
        else:
            raise ValueError(f"Unsupported ConfigKey: {config_key}")
