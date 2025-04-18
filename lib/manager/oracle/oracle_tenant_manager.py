import logging

from lib.config.config_loader import get_config_section
from lib.manager.oracle.oracle_manager import OracleManager
from lib.models.db.oracle.oracle_connect_info import ORACLE_CONNECT_KEYS, get_oracle_connect_info

logging.basicConfig(level=logging.DEBUG)


class OracleTenantManager(OracleManager):

    def __init__(self, yaml_loader, env_type, db_type, vendor):
        super().__init__()
        self.yaml_loader = yaml_loader
        self.env_type = env_type
        self.db_type = db_type
        self.vendor = vendor
        self.config_section = get_config_section(self.env_type, self.db_type, self.vendor)
        self.connect_info = get_oracle_connect_info(self.yaml_loader, self.config_section)

        self.session = None

    def is_valid_connect_info(self):
        if self.connect_info is None:
            return False

        return self.connect_info.is_valid()

    def ensure_connect_info_key(self, config_loader, key):
        value = self.connect_info.get_value_by_config_key(key)

        if value:
            return True

        value_new = config_loader.get_config(self.config_section, key.key)
        if value_new:
            self.connect_info.set_value_by_config_key(key, value_new)
            return True

        value_new = config_loader.ensure_config(
            self.config_section, key.key, f"{self.env_type}:{self.db_type}", f"Input {key.key}!", key.is_secure)
        if value_new:
            self.connect_info.set_value_by_config_key(key, value_new)
            return True

        return False

    """
    Connect Info 를 체크하고 일부 값이 없는 경우 config 로 set
    """

    def ensure_connect_info(self, config_loader):
        if self.connect_info is None:
            logging.error("connect_info is None")
            return False

        if self.is_valid_connect_info():
            # connect info 가 모두 있으면 True
            return True

        for config_key in ORACLE_CONNECT_KEYS:
            self.ensure_connect_info_key(config_loader, config_key)

        return self.is_valid_connect_info()

    def get_db_session(self):
        return super().get_db_session(self.connect_info)
