from lib.manager.log.base.base_log_search_scheduler import BaseLogSearchScheduler
from lib.models.constants.const_response import RespMessage
from lib.models.constants.log_step import LogStepSearch
from lib.models.constants.service_name_type import ServiceType


class LogSearchScheduler(BaseLogSearchScheduler):
    def __init__(self, manager, yaml_loader, config_loader):
        super().__init__(manager, yaml_loader, config_loader)
        self.step_connect_info = None
        self.step_log_path = None

    # log search step 을 리턴함
    def get_step_connect_infos(self, main_step):
        if main_step == LogStepSearch.GATEWAY:
            self.step_connect_infos = self.get_connect_infos_by_service_name(self.service_name)
            return self.step_connect_infos
        elif main_step == LogStepSearch.API:
            self.service_name = ServiceType.API.value.service_name
            self.step_connect_infos = self.get_connect_infos_by_service_name(self.service_name)
            return self.step_connect_infos
        elif main_step == LogStepSearch.ECHO:
            self.service_name = ServiceType.ECHO.value.service_name
            self.step_connect_infos = self.get_connect_infos_by_service_name(self.service_name)
            return self.step_connect_infos


        return self.step_connect_infos

    def ensure_step_connect_info(self):
        print("")

    def get_step_log_path(self, step):
        return self.step_log_path

    # step 을 스케줄링
    def schedule_steps(self):
        if self.env is None:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " env : env=" + self.tenant_name)

        if self.keyword is None:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " keyword")
            return response

        if self.service_name is None:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " service_name=" + self.service_name)

        self.all_main_steps = []
        if self.service_name == ServiceType.GATEWAY.value.service_name:
            self.all_main_steps.append(LogStepSearch.GATEWAY)
            self.all_main_steps.append(LogStepSearch.API)
            self.all_main_steps.append(LogStepSearch.ECHO)
        else:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " step : service=" + self.service_name)

        return self.get_success_response()
