from enum import Enum, unique

from lib.models.constants.log_parser_type import LogParserType
from lib.models.fabric.service_info import ServiceInfo


@unique
class ServiceType(Enum):
    GATEWAY = ServiceInfo(
        "gateway", "vagrant",
        None,
        "/home/vagrant/gateway.log",
        None,
        LogParserType.ECHO)
    API = ServiceInfo(
        "api", "vagrant",
        None,
        "/home/vagrant/api.lo",
        None,
        LogParserType.ECHO)
    ECHO = ServiceInfo(
        "echo", "vagrant",
        None,
        "/home/vagrant/echo.log",
        None,
        LogParserType.ECHO)
