from enum import Enum, unique

@unique
class LogStepSearch(Enum):
    GATEWAY = "/home/vagrant/gateway.log"
    API = "/home/vagrant/api.log"
    ECHO = "/home/vagrant/echo.log"

# Log Step : Path
@unique
class LogStepPath(Enum):
    ACCESS_PATH = "access-path"
    DEBUG_PATH = "debug-path"
    INFO_PATH = "info-path"
