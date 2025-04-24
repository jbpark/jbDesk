from lib.manager.test.base.base_service_test_manager import BaseServiceTestManager


class ServiceTestManager(BaseServiceTestManager):
    def __init__(self, env):
        super().__init__(env)

    def get_test_result(self):
        result = []

        return result