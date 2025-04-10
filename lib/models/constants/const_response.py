from enum import Enum, unique

# Define an enumeration class with custom values
@unique
class RespStatus(Enum):
    SUCCESS = "Success"
    FAILED = 'Failed'

@unique
class RespMessage(Enum):
    SUCCESS = "Success"
    NOT_FOUND = "Not found"
    INVALID = "Invalid"
    NOT_UPDATED = "Not updated"
    FAILED_COUNT_SAME = "Failed_count is same"
    DELETED_DATA_CANNOT_UPDATE = "Deleted data cannot be updated."
    JSON_DECODE_ERROR = "Json decode error"