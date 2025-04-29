from lib.fabric.command.fab_ssh_command_shell import FabSshCommandShell
from lib.manager.fabric.base.base_fab_manager import BaseFabManager
from lib.models.constants.const_response import RespStatus
import logging
import warnings

from cryptography.utils import CryptographyDeprecationWarning

# fabric3 패키지는 paramiko 3.0 미만만 지원한다고 명시되어 있는데
# paramiko 3.0 은 다음 에러가 발생하여 에러 경고를 무시하도록 추가함
# paramiko\pkey.py:82: CryptographyDeprecationWarning: TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from lib.util.config_util import load_service_connect_infos_from_yaml

from lib.models.log.respone.log_search_response import LogSearchResponse
from lib.models.constants.env_type import ENV_DEV
from lib.models.constants.const_response import RespStatus, RespMessage

from lib.fabric.log.fab_ssh_log_shell import FabSshLogShell
from lib.manager.fabric.ssh_manager import SshManager
from lib.manager.process.manger_holder import get_process_manager
from lib.models.fabric.fab_connect_info import FabConnectInfo

from multiprocessing import Process, Lock

class FabCommandManager(BaseFabManager):
    def __init__(self, env, keyword, service_name, level):
        super().__init__(env, keyword, service_name, level)

    def get_result(self, scheduler):
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

        response.logs = self.get_fab_result()
        response.index = self.total
        response.total = self.total
        return response

    def get_fab_result(self):
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
                fab_ssh_command_shell = FabSshCommandShell(lock, self.scheduler, fab_connect_info)

                p = Process(target=fab_ssh_command_shell.get_command_result, args=(index, return_dict, keyword))

                p.start()
                process_list.append(p)

            for p in process_list:
                p.join()

            parsed_logs = []

            # for index, item in enumerate(service_connect_infos):
            #
            #     if not return_dict[index]:
            #         logging.info("not return_dict[index]")
            #         continue
            #
            #     lines = return_dict[index].split('\n')
            #     for line in lines:
            #         log = self.parse_log(parser_name, item.get_host_name(), line)
            #         if log:
            #             display_log = log.get_display_log()
            #             logs.append(display_log)
            #             parsed_logs.append(log)
            #
            # self.scheduler.setLogs(parsed_logs)

        return logs