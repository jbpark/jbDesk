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
        return self.service.service_name

    def get_parser_name(self):
        return self.service.parser_name

    def get_private_ip(self):
        if self.host is None:
            return None

        return self.host.private_ip

    def get_public_ip(self):
        if self.host is None:
            return None

        return self.host.public_ip

    def get_gateway_private_ip(self):
        if self.gateway is None:
            return None

        return self.gateway.private_ip

    def get_gateway_public_ip(self):
        if self.gateway is None:
            return None

        return self.gateway.public_ip

    def set_user_name(self, user_name):
        if self.host is None:
            return

        self.host.user_name = user_name

    def set_password(self, password):
        if self.host is None:
            return

        self.host.password = password

    def set_gateway_user_name(self, user_name):
        if self.gateway is None:
            return

        self.gateway.user_name = user_name

    def set_gateway_password(self, password):
        if self.gateway is None:
            return

        self.gateway.password = password

    def get_gateway_password(self):
        if self.gateway is None:
            return

        return self.gateway.password

    def get_host_string(self):
        if self.env == ENV_DEV:
            return f"{self.host.user_name}@{self.host.private_ip}"
        else:
            return f"{self.host.user_name}@{self.host.public_ip}"

    def get_host_ip(self):
        if self.env == ENV_DEV:
            return self.host.private_ip
        else:
            return self.host.public_ip

    def get_host_name(self):
        return f"{self.host.host_name}"

    def get_gateway_host_name(self):
        if self.gateway is None:
            return None

        return f"{self.gateway.host_name}"

    def get_gateway_string(self):
        if self.gateway is None:
            return None

        if self.env == ENV_DEV:
            return f"{self.gateway.user_name}@{self.gateway.private_ip}"
        else:
            return f"{self.gateway.user_name}@{self.gateway.public_ip}"

    def get_gateway_user_name(self):
        if self.gateway is None:
            return None

        return self.gateway.user_name

    def get_host_user_name(self):
        if self.host is None:
            return None

        return self.host.user_name

    def get_host_password(self):
        if self.host is None:
            return None

        return self.host.password

    def get_gateway_ip(self):
        if self.gateway is None:
            return None

        if self.env == ENV_DEV:
            return self.gateway.private_ip
        else:
            return self.gateway.public_ip

    def get_decode_password(self):
        return self.host.get_decode_password()

    def get_log_paths(self, level):
        result = []
        if level == LogLevel.ALL.value:
            if self.service.log_path_access is not None:
                result.append(self.service.log_path_access)

            if self.service.log_path_level is not None:
                result.append(self.service.log_path_level.replace('{level}', LogLevel.DEBUG.value))
                result.append(self.service.log_path_level.replace('{level}', LogLevel.INFO.value))
        elif level == LogLevel.ACCESS.value:
            if self.service.log_path_access is not None:
                result.append(self.service.log_path_access)
        else:
            if self.service.log_path_level is not None:
                result.append(self.service.log_path_level.replace('{level}', level))

        return result
