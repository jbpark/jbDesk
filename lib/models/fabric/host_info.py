from lib.util.encoding_util import decrypt_cipher_text


class HostInfo:
    def __init__(self, host_name, private_ip, public_ip, user, password, gateway):
        self.host_name = host_name
        self.private_ip = private_ip
        self.public_ip = public_ip
        self.user = user
        self.password = password
        self.gateway = gateway

    def get_decode_password(self):
        return decrypt_cipher_text(self.password)


class ServiceInfo:
    def __init__(self, service_name, user_name, log_path_access, log_path_level, urls, parser_name):
        self.service_name = service_name
        self.user_name = user_name
        self.log_path_access = log_path_access
        self.log_path_level = log_path_level
        self.urls = urls
        self.parser_name = parser_name


def get_host_info_by_name(host_infos, host_name):
    for host_info in host_infos:
        if host_info.host_name == host_name:
            return host_info

    return None
