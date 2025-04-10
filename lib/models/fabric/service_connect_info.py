from lib.models.constants.env_type import ENV_DEV
from lib.models.log.log_level import LogLevel


class ServiceConnectInfo:
    def __init__(self, env, project, group, service, host, gateway):
        self.env = env
        self.project = project
        self.group = group
        self.service = service
        self.host = host
        self.gateway = gateway

    def get_service_name(self):
        return self.service.value.service_name

    def get_parser_name(self):
        return self.service.value.parser_name

    def get_host_string(self):
        if self.env == ENV_DEV:
            return f"{self.host.value.user}@{self.host.value.private_ip}"
        else:
            return f"{self.host.value.user}@{self.host.value.public_ip}"

    def get_host_name(self):
        return f"{self.host.value.host_name}"

    def get_gateway_string(self):
        if self.env == ENV_DEV:
            return f"{self.gateway.value.user}@{self.gateway.value.private_ip}"
        else:
            return f"{self.gateway.value.user}@{self.gateway.value.public_ip}"

    def get_decode_password(self):
        return self.host.value.get_decode_password()

    def get_log_paths(self, level):
        result = []
        if level == LogLevel.ALL.value:
            result.append(self.service.value.log_path_access)
            result.append(self.service.value.log_path_level.replace('{level}', LogLevel.DEBUG.value))
            result.append(self.service.value.log_path_level.replace('{level}', LogLevel.INFO.value))
        elif level == LogLevel.ACCESS.value:
            result.append(self.service.value.log_path_access)
        else:
            result.append(self.service.value.log_path_level.replace('{level}', level))

        return result
