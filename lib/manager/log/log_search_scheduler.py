from lib.manager.log.base.base_log_search_scheduler import BaseLogSearchScheduler


class LogSearchScheduler(BaseLogSearchScheduler):
    def __init__(self, manager, yaml_loader, config_loader):
        super().__init__(manager, yaml_loader, config_loader)
        self.step_connect_info = None
        self.step_log_path = None

    # log search step 을 리턴함
    def get_step_connect_infos(self, step):
        return self.step_connect_infos

    def ensure_step_connect_info(self):
        print("")

    def get_step_log_path(self, step):
        return self.step_log_path
