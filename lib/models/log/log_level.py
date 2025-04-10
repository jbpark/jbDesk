from enum import Enum, unique

@unique
class LogLevel(Enum):
    ALL = "all"
    ACCESS = "access"
    DEBUG = "debug"
    INFO = "info"
    ERROR = "error"