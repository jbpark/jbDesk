from lib.models.fabric.host_info import ServiceInfo, get_host_info_by_name, HostInfo
from lib.models.fabric.service_connect_info import ServiceConnectInfo


def load_host_infos_from_yaml(yaml_loader):
    data = yaml_loader.load_config()

    host_info_list = []

    for key, value in data.items():
        if key.startswith("HOST."):
            host_name = key.split("HOST.")[1]
            private_ip = value.get("private_ip", "")
            public_ip = value.get("public_ip", "")
            user = value.get("username", "")
            password = value.get("password", "")
            gateway = value.get("gateway", "")

            host_info = HostInfo(
                host_name=host_name,
                private_ip=private_ip,
                public_ip=public_ip,
                user=user,
                password=password,
                gateway=gateway
            )
            host_info_list.append(host_info)

    return host_info_list


def get_value_with_default(d: dict, key: str, default_value):
    # 키가 없거나, 값이 None이거나 빈 문자열이면 기본값 할당
    if key not in d or d[key] is None or d[key] == "":
        return default_value

    return d[key]


def load_service_connection_infos_from_yaml(yaml_loader):
    host_infos = load_host_infos_from_yaml(yaml_loader)

    data = yaml_loader.load_config()

    service_connection_infos = []

    for key, value in data.items():
        if key.startswith("SERVICE."):
            service_host = key.split("SERVICE.")[1]
            parts = service_host.split('.', 1)
            service_name = parts[0]
            host_name = parts[1] if len(parts) > 1 else None
            env = value.get("env", "")
            project = value.get("project", "")
            group = value.get("group", "")
            tp_user = value.get("tp_user", "")
            gateway_name = value.get("gateway", "")
            access_log = value.get("access_log", "")
            level_log = value.get("level_log", "")
            parser = get_value_with_default(value, "parser", "middleware")

            service = ServiceInfo(service_name, tp_user, access_log, level_log, None, parser)
            host = get_host_info_by_name(host_infos, host_name)
            gateway = get_host_info_by_name(host_infos, gateway_name)

            service_connection_info = ServiceConnectInfo(
                env=env.upper(),
                project=project,
                group=group,
                service=service,
                host=host,
                gateway=gateway
            )
            service_connection_infos.append(service_connection_info)

    return service_connection_infos
