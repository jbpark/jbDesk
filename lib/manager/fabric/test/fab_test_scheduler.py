from lib.manager.fabric.base.base_fab_scheduler import BaseFabScheduler
from lib.models.constants.test_step import TestStep
from lib.models.constants.const_response import RespMessage
from lib.models.constants.log_step import LogStepSearch
from lib.models.constants.service_name_type import ServiceType

class FabTestScheduler(BaseFabScheduler):
    def __init__(self, manager, yaml_loader, config_loader):
        super().__init__(manager, yaml_loader, config_loader)
        self.step_connect_info = None
        self.step_log_path = None

    # 전체 step 시 어떤 일을 할지 스케줄링
    def schedule_steps(self):
        if self.env is None:
            return self.get_failed_response(RespMessage.NOT_FOUND.value + " env : env=" + self.tenant_name)

        self.all_main_steps = []
        # OS 정보를 구함
        self.all_main_steps.append(TestStep.OS_INFO)

        return self.get_success_response()

    def get_step_connect_infos(self, main_step):
        if main_step == TestStep.OS_INFO:
            # OS Info 의 경우 전체 host 의 connect info 를 리턴
            self.step_connect_infos = self.get_connect_infos_by_host()
            return self.step_connect_infos
        else:
            return None

        return self.step_connect_infos
