from enum import Enum, unique

# Test Step
@unique
class TestResultType(Enum):
    OS_INFO = "os_info" # OS 정보를 구함