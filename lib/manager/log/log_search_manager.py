import logging
import warnings

from cryptography.utils import CryptographyDeprecationWarning

from lib.manager.log.base.base_log_search_manager import BaseLogSearchManager
from lib.models.constants.log_parser_type import LogParserType
from lib.models.constants.service_name_type import ServiceType
from lib.parser.log_parser import LogParser

# fabric3 패키지는 paramiko 3.0 미만만 지원한다고 명시되어 있는데
# paramiko 3.0 은 다음 에러가 발생하여 에러 경고를 무시하도록 추가함
# paramiko\pkey.py:82: CryptographyDeprecationWarning: TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from lib.fabric.log.fab_ssh_log_shell import FabSshLogShell
from lib.manager.fabric.ssh_manager import SshManager
from lib.manager.process.manger_holder import get_process_manager
from lib.models.fabric.fab_connect_info import FabConnectInfo

from multiprocessing import Process, Lock


class LogSearchManager(BaseLogSearchManager):
    def __init__(self, env, keyword, service_name, level):
        super().__init__(env, keyword, service_name, level)

    @staticmethod
    def parse_log(parser_name, host, line):
        parser = LogParser()
        return parser.parse_log(parser_name, host, line)

    def get_logs(self):
        keyword = self.keyword

        process_manager = get_process_manager()
        return_dict = process_manager.dict()

        lock = Lock()
        process_list = []
        logs = []

        logging.info("exist_main_step")
        while self.scheduler.exist_main_step():
            current_main_step = self.scheduler.get_next_main_step()
            if current_main_step is None:
                logging.info("current_main_step is None")
                break

            self.scheduler.schedule_sub_steps()

            service_connect_infos = self.scheduler.get_step_connect_infos(current_main_step)
            if service_connect_infos is None:
                logging.info("service_connect_infos is None")
                break

            for index, service_connect_info in enumerate(service_connect_infos):
                ssh_manager = SshManager(self.yaml_loader, self.config_loader)
                if not ssh_manager.ensure_service_connect_info(service_connect_info):
                    logging.warn("not ssh_manager.ensure_service_connect_info(service_connect_info")
                    break

                fab_connect_info = FabConnectInfo(service_connect_info.get_gateway_ip(),
                                                  service_connect_info.get_gateway_user_name(),
                                                  service_connect_info.get_gateway_password(),
                                                  service_connect_info.get_host_ip(),
                                                  service_connect_info.get_host_user_name(),
                                                  service_connect_info.get_host_password())
                fab_ssh_log_shell = FabSshLogShell(lock, self.scheduler, fab_connect_info)

                p = Process(target=fab_ssh_log_shell.get_search_log, args=(index, return_dict, keyword))

                p.start()
                process_list.append(p)

            for p in process_list:
                p.join()

            parsed_logs = []

            for index, item in enumerate(service_connect_infos):

                if not return_dict[index]:
                    logging.info("not return_dict[index]")
                    continue

                if item.service.service_name == ServiceType.GATEWAY.value.service_name or \
                        item.service.service_name == ServiceType.API.value.service_name or \
                        item.service.service_name == ServiceType.ECHO.value.service_name:
                    parser_name = LogParserType.ECHO
                else:
                    parser_name = item.get_parser_name()

                lines = return_dict[index].split('\n')
                for line in lines:
                    log = self.parse_log(parser_name, item.get_host_name(), line)
                    if log:
                        # search_log = SearchLog()
                        # search_log.searchRequest = search_request
                        # search_log.host = host.name
                        # search_log.log = line
                        # search_log.save()
                        display_log = log.get_display_log()
                        # display_log.id = search_log.pk
                        logs.append(display_log)
                        parsed_logs.append(log)

            self.scheduler.setLogs(parsed_logs)

        return logs
