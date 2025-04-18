from lib.models.constants.const_response import RespStatus, RespMessage
from lib.models.log.respone.log_search_response import LogSearchResponse
from lib.util.config_util import load_service_connect_infos_from_yaml, load_ssh_user_infos_from_yaml


class BaseLogSearchScheduler:
    def __init__(self, manager, yaml_loader, config_loader):
        self.manager = manager
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.env = manager.env
        self.keyword = manager.keyword
        self.service_name = manager.service_name
        self.level = manager.level
        self.logs = None
        self.index = 0
        self.total = 0

        # 전체 main steps
        self.all_main_steps = []

        # 현재 main step
        self.current_main_step = None

        # 전체 sub steps
        self.all_sub_steps = None

        # 현재 sub step
        self.current_sub_step = None

        self.step_connect_infos = None

        self.all_connect_infos = self.get_all_connect_infos()
        self.env_connect_infos = self.get_env_connect_infos()
        self.ssh_connect_infos = self.get_ssh_connect_infos()

    def get_all_connect_infos(self):
        if self.env is None:
            return None

        return load_service_connect_infos_from_yaml(self.yaml_loader)

    def get_env_connect_infos(self):
        env_connect_infos = []

        for item in self.all_connect_infos:
            if item.env.upper() != self.env.upper():
                continue

            env_connect_infos.append(item)

        return env_connect_infos

    def exist_main_step(self):
        if self.all_main_steps:
            return True
        else:
            return False

    def exist_sub_step(self):
        if self.all_sub_steps:
            return True
        else:
            return False

    # log search step 을 리턴함
    def get_current_main_step(self):
        return self.current_main_step
    
    # sub steps 를 스케줄링
    def schedule_sub_steps(self):
        print("schedule_sub_steps")

    def get_next_main_step(self):
        if not self.all_main_steps:
            return None

        self.current_main_step = self.all_main_steps.pop(0)
        return self.current_main_step

    def get_all_sub_steps(self):
        return self.all_sub_steps

    def get_next_sub_step(self):
        if not self.all_sub_steps:
            return None

        self.current_sub_step = self.all_sub_steps.pop(0)
        return self.current_sub_step

    # log search step 을 리턴함
    def get_step_connect_infos(self, step):
        return self.step_connect_infos

    def ensure_step_connect_info(self):
        print("")

    def get_step_log_path(self, step):
        return self.step_log_path

    def get_ssh_connect_infos(self):
        return load_ssh_user_infos_from_yaml(self.yaml_loader)

    def setLogs(self, logs):
        self.logs = logs

    def get_failed_response(self, message):
        response = LogSearchResponse()
        response.command_type = "log"
        response.status = RespStatus.FAILED.value
        response.message = message
        response.index = self.index
        response.total = self.total
        return response

    def get_success_response(self):
        response = LogSearchResponse()
        response.command_type = "log"
        response.status = RespStatus.SUCCESS.value
        response.message = RespMessage.SUCCESS.value
        response.index = self.index
        response.total = self.total
        return response

    def get_connect_infos_by_service_name(self, service_name):
        connect_infos = []

        for item in self.env_connect_infos:
            if item.service.service_name != service_name:
                continue

            connect_infos.append(item)

        return connect_infos
