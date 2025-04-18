from lib.models.constants.config_key import ConfigKey
from lib.models.fabric.host_info import get_host_info_by_name, HostInfo
from lib.models.fabric.service_connect_info import ServiceConnectInfo
from lib.models.fabric.service_info import ServiceInfo
from lib.models.fabric.ssh_user_info import SshUserInfo


def load_host_infos_from_yaml(yaml_loader):
    data = yaml_loader.load_config()

    hosts = data.get("HOST")
    list = []
    for index, item in enumerate(hosts):
        host_name = item.get(ConfigKey.KEY_HOST_NAME.key, "")
        private_ip = item.get(ConfigKey.KEY_PRIVATE_IP.key, "")
        public_ip = item.get(ConfigKey.KEY_PUBLIC_IP.key, "")
        user_name = item.get(ConfigKey.KEY_USER_NAME.key, "")
        password = item.get(ConfigKey.KEY_PASSWORD.key, "")
        gateway = item.get(ConfigKey.KEY_GATEWAY.key, "")

        host_info = HostInfo(
            host_name=host_name,
            private_ip=private_ip,
            public_ip=public_ip,
            user_name=user_name,
            password=password,
            gateway=gateway
        )
        list.append(host_info)

    return list


def get_value_with_default(d: dict, key: str, default_value):
    # 키가 없거나, 값이 None이거나 빈 문자열이면 기본값 할당
    if key not in d or d[key] is None or d[key] == "":
        return default_value

    return d[key]


def load_service_connect_infos_from_yaml(yaml_loader):
    host_infos = load_host_infos_from_yaml(yaml_loader)

    data = yaml_loader.load_config()
    services = data.get("SERVICE")

    service_connect_infos = []

    for key, services in data.items():
        if key == "SERVICE":
            for service_name, hosts in services.items():
                for item in hosts:
                    host_name = item.get(ConfigKey.KEY_HOST_NAME.key, "")
                    env = item.get(ConfigKey.KEY_ENV.key, "")
                    project = item.get(ConfigKey.KEY_PROJECT.key, "")
                    group = item.get(ConfigKey.KEY_GROUP.key, "")
                    service = ServiceInfo(service_name, None, None, None, None, None)
                    host = get_host_info_by_name(host_infos, host_name)
                    if host is not None:
                        gateway_name = host.gateway
                        gateway = get_host_info_by_name(host_infos, gateway_name)
                    else:
                        gateway = None

                    service_connect_info = ServiceConnectInfo(
                        env=env.upper(),
                        project=project,
                        group=group,
                        service=service,
                        host=host,
                        gateway=gateway
                    )
                    service_connect_infos.append(service_connect_info)

    return service_connect_infos


def load_ssh_user_infos_from_yaml(yaml_loader):
    data = yaml_loader.load_config()
    users = data.get(f"SSH")
    list = []
    for index, item in enumerate(users):
        ssh_user_info = SshUserInfo(index,
                                    item.get(ConfigKey.KEY_USER_NAME.key, ""),
                                    item.get(ConfigKey.KEY_PASSWORD.key, ""))
        list.append(ssh_user_info)

    return list

def get_ssh_user_info_from_config(config_loader, host_name):
    user_name = config_loader.get_config(f"SSH.{host_name}", ConfigKey.KEY_USER_NAME.key)
    password = config_loader.get_config(f"SSH.{host_name}", ConfigKey.KEY_PASSWORD.key)

    if user_name is None or password is None:
        return None

    return SshUserInfo(0, user_name, password)
