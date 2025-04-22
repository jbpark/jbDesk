import logging

from lib.models.constants.config_key import ConfigKey
from lib.models.fabric.ssh_user_info import SshUserInfo
from lib.util.config_util import load_ssh_user_infos_from_yaml, get_ssh_user_info_from_config
from lib.util.ssh_util import get_ssh_user_info

logging.basicConfig(level=logging.DEBUG)


class SshManager:
    def __init__(self, yaml_loader, config_loader):
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.ssh_user_infos = self.get_ssh_user_infos()

    def get_ssh_user_infos(self):
        return load_ssh_user_infos_from_yaml(self.yaml_loader)

    def get_ssh_user_index(self, ssh_user_info):
        if ssh_user_info is None:
            return 0

        if ssh_user_info.user_name is None or ssh_user_info.password is None:
            return 0

        for item in self.ssh_user_infos:
            if item.user_name == ssh_user_info.user_name and item.password == ssh_user_info.password:
                return item.index

        return 0

    def ensure_service_connect_info(self, service_connect_info, use_private_ip=True, check_user=False):
        ssh_user_info = get_ssh_user_info_from_config(self.config_loader, service_connect_info.get_host_name())
        if ssh_user_info is None:
            exist_config = False
        else:
            exist_config = True
        index = self.get_ssh_user_index(ssh_user_info)

        if use_private_ip:
            host_ip = service_connect_info.get_private_ip()
        else:
            host_ip = service_connect_info.get_public_ip()

        if check_user:
            ssh_user_info = get_ssh_user_info(self.ssh_user_infos, host_ip, index)

        if ssh_user_info is None:
            ssh_user_info = get_ssh_user_info(self.ssh_user_infos, host_ip, index)

        if ssh_user_info is None:
            return False

        if not exist_config:
            self.config_loader.set_config(f"SSH.{service_connect_info.get_host_name()}", ConfigKey.KEY_USER_NAME.key,
                                          ssh_user_info.user_name)
            self.config_loader.set_config(f"SSH.{service_connect_info.get_host_name()}", ConfigKey.KEY_PASSWORD.key,
                                          ssh_user_info.password)

        service_connect_info.set_user_name(ssh_user_info.user_name)
        service_connect_info.set_password(ssh_user_info.password)

        # gateway
        gateway_host_name = service_connect_info.get_gateway_host_name()
        if gateway_host_name is not None:
            ssh_user_info = get_ssh_user_info_from_config(self.config_loader, gateway_host_name)
            if ssh_user_info is None:
                exist_config = False
            else:
                exist_config = True
            index = self.get_ssh_user_index(ssh_user_info)

            if use_private_ip:
                host_ip = service_connect_info.get_gateway_private_ip()
            else:
                host_ip = service_connect_info.get_gateway_public_ip()

            if check_user:
                ssh_user_info = get_ssh_user_info(self.ssh_user_infos, host_ip, index)

            if ssh_user_info is None:
                return False

            if not exist_config:
                self.config_loader.set_config(f"SSH.{service_connect_info.get_gateway_host_name()}",
                                              ConfigKey.KEY_USER_NAME.key,
                                              ssh_user_info.user_name)
                self.config_loader.set_config(f"SSH.{service_connect_info.get_gateway_host_name()}",
                                              ConfigKey.KEY_PASSWORD.key,
                                              ssh_user_info.password)

            service_connect_info.set_gateway_user_name(ssh_user_info.user_name)
            service_connect_info.set_gateway_password(ssh_user_info.password)

        return True

    def get_config_key(self, host_name, key):
        value = self.config_loader.get_config(f"SSH.{host_name}", key.key)
        if value is not None:
            return value

        value_new = self.config_loader.ensure_config(
            f"{self.env.upper()}.{host_name}", key.key, f"{self.env.upper()}.{host_name}", f"Input {key.key}!",
            key.is_secure)
        if value_new is not None:
            return value_new

        return None

    def get_ssh_user_info(self, host_name):
        user_name = self.get_config_key(host_name, ConfigKey.KEY_USER_NAME)
        password = self.get_config_key(host_name, ConfigKey.KEY_PASSWORD)
        if user_name is not None and password is not None:
            return SshUserInfo(0, user_name, password)

    # def ensure_host_info(self, host_info, use_private_ip = True):
    #     if use_private_ip:
    #         if is_none_or_empty(host_info.private_ip):
    #             logging.error("private_ip is None")
    #             return False
    #     else:
    #         if is_none_or_empty(host_info.public_ip):
    #             logging.error("public_ip is None")
    #             return False
    #
    #     if is_none_or_empty(host_info.host_name):
    #         logging.error("host_name is None")
    #         return False
    #
    #     if is_none_or_empty(host_info.user_name):
    #         user_name = self.get_config_key(host_info.host_name, ConfigKey.KEY_USER_NAME)
    #         if user_name is not None:
    #             host_info.user_name = user_name
    #         else:
    #             logging.error("user_name is None")
    #             return False
    #
    #     if is_none_or_empty(host_info.password):
    #         password = self.get_config_key(host_info.host_name, ConfigKey.KEY_PASSWORD)
    #         if password is not None:
    #             host_info.password = password
    #         else:
    #             logging.error("password is None")
    #             return False
    #
    #     return True
