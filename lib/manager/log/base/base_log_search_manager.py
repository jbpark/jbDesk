import logging
import warnings

from cryptography.utils import CryptographyDeprecationWarning

# fabric3 패키지는 paramiko 3.0 미만만 지원한다고 명시되어 있는데
# paramiko 3.0 은 다음 에러가 발생하여 에러 경고를 무시하도록 추가함
# paramiko\pkey.py:82: CryptographyDeprecationWarning: TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from lib.fabric.log.fab_ssh_log_shell import FabSshLogShell
from lib.manager.fabric.ssh_manager import SshManager
from lib.manager.process.manger_holder import get_process_manager
from lib.models.constants.log_step import LogStepSearch
from lib.models.fabric.fab_connect_info import FabConnectInfo
from lib.util.config_util import load_service_connect_infos_from_yaml

from lib.models.log.log_level import LogLevel
from lib.models.log.respone.log_search_response import LogSearchResponse
from lib.models.constants.env_type import ENV_DEV
from lib.models.constants.const_response import RespStatus, RespMessage
from multiprocessing import Process, Lock

class BaseLogSearchManager:
    def __init__(self, env, keyword, service_name, level):
        self.env = env.upper()
        self.keyword = keyword
        self.service_name = service_name
        self.level = level
        self.parser_name = None
        self.service = None
        self.step = None
        self.all_connect_infos = None
        self.service_connect_infos = []
        self.scheduler = None
        self.total = None
        self.yaml_loader = None
        self.config_loader = None

    def add_service_connect_info_by_group(self, group):
        for item in self.all_connect_infos:
            if item.env != self.env:
                continue

            if item.service.group != group:
                continue

            self.service_connect_infos.append(item)

    def add_service_connect_info_by_service_name(self, service_name):
        for item in self.all_connect_infos:
            if item.env != self.env:
                continue

            if item.service.service_name != service_name:
                continue

            self.service_connect_infos.append(item)

    def set_service_connect_infos(self, yaml_loader):
        if self.service is None:
            return

        self.all_connect_infos = load_service_connect_infos_from_yaml(yaml_loader)

        for item in self.all_connect_infos:
            if item.env != self.env:
                continue

            if item.service.service_name != self.service.value.service_name:
                continue

            self.service_connect_infos.append(item)

        print("set_service_connect_infos")

    def get_passwords(self):
        passwords = {}

        for item in self.service_connect_infos:
            if item.host is None:
                continue

            if self.env == ENV_DEV:
                host_ip = item.host.private_ip
            else:
                host_ip = item.host.public_ip

            passwords[host_ip] = item.host.get_decode_password()

        return passwords

    def get_passwords(self, connect_info):
        passwords = {}

        if connect_info.gateway is not None:
            if self.env == ENV_DEV:
                host_ip = connect_info.gateway.private_ip
            else:
                host_ip = connect_info.gateway.public_ip

            passwords[host_ip] = connect_info.gateway.get_decode_password()

        if self.env == ENV_DEV:
            host_ip = connect_info.host.private_ip
        else:
            host_ip = connect_info.host.public_ip

        passwords[host_ip] = connect_info.host.get_decode_password()

        return passwords

    @staticmethod
    def parse_log(parser_name, host, line):
        print("parse_log")

    def get_log_info(self, scheduler):
        self.scheduler = scheduler
        self.yaml_loader = scheduler.yaml_loader
        self.config_loader = scheduler.config_loader
        response = self.scheduler.schedule_steps()
        if response.status != RespStatus.SUCCESS.value:
            logging.warn(f"response:{response}")
            return response

        response = LogSearchResponse()
        response.command_type = "log"
        response.status = RespStatus.SUCCESS.value
        response.message = RespMessage.SUCCESS.value
        if self.step is not None:
            response.step = self.step.value

        response.logs = self.get_logs()
        response.index = self.total
        response.total = self.total
        return response
