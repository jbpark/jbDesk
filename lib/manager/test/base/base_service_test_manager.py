from lib.models.test.service_test_info import ServiceTestInfo
from lib.util.config_util import load_service_connect_infos_from_yaml


class BaseServiceTestManager:
    def __init__(self, env):
        self.env = env.upper()
        self.all_connect_infos = None
        self.service_test_infos = []

    def load_info(self, yaml_loader):
        self.all_connect_infos = load_service_connect_infos_from_yaml(yaml_loader)

        for item in self.all_connect_infos:
            if item.env != self.env:
                continue

            service_test_info = ServiceTestInfo(item.service.service_name)

            self.service_test_infos.append(service_test_info)

        print("load_info")
