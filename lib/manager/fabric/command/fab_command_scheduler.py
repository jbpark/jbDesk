from lib.manager.fabric.base.base_fab_scheduler import BaseFabScheduler
from lib.models.constants.command_step import CommandStep
from lib.models.constants.const_response import RespMessage
from lib.models.constants.log_step import LogStepSearch
from lib.models.constants.service_name_type import ServiceType

class FabCommandScheduler(BaseFabScheduler):
    def __init__(self, manager, yaml_loader, config_loader):
        super().__init__(manager, yaml_loader, config_loader)
        self.step_connect_info = None
        self.step_log_path = None

    def schedule_steps(self):
        if self.env is None:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " env : env=" + self.tenant_name)

        self.all_main_steps = []
        self.all_main_steps.append(CommandStep.OS_INFO)

        return self.get_success_response()

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
