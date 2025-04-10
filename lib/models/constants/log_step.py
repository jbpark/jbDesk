from enum import Enum, unique

@unique
class LogStepSearch(Enum):
    FIND_SERVICE = "Find Service"
    FIND_LOG = "Find Log"

# Log Step : Path
@unique
class LogStepPath(Enum):
    ACCESS_PATH = "access-path"
    DEBUG_PATH = "debug-path"
    INFO_PATH = "info-path"