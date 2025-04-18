from lib.models.log.log_pattern import LogPattern


class RegPattern:
    WORD = r'(?P<%s>\S+)'
    B_WORD = r'\[(?P<%s>\S+)\]'
    B_WORD_AST = r'\[(?P<%s>\S*)\]'
    TIME_RECEIVED = r'\[(?P<%s>[\w:/]+\s[+\-]\d{4})\]'
    TIMESTAMP = r'(?P<%s>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{1,3})'
    REQUEST_FIRST_LINE = r'"(?P<%s>(\S+) (\S+)\s*(\S+)\s*)"'
    STATUS = r'(?P<%s>\d{3})'
    USER_AGENT = r'"(?P<%s>(\S+)\s*(\S+))"'
    DQ_WORD = r'"(?P<%s>\S+)"'
    DIGIT_MS = r'(?P<%s>\d{1,}ms)'
    LEVEL = r'(?P<%s>(INFO|ERROR|WARN|TRACE|DEBUG|FATAL))'
    B_TRACE_SPAN_PARENT_ID = r'\[(?P<%s>[A-Za-z0-9]*,[A-Za-z0-9]*,[A-Za-z0-9]*)\]'
    ANY = r'(?P<%s>.*)'
    RESOURCE = r'resource=(?P<%s>\d{1,5}),'
    STATUS_CODE = r'"status_code":"(?P<%s>[A-Za-z0-9]*)"'
    REQUEST_ID = r'"request_id":"(?P<%s>[A-Za-z0-9]*)"'

    SPACE = LogPattern(r'\s', None)
    SPACE_MORE = LogPattern(r'\s+', None)
    COLON = LogPattern(r':', None)
    HYPHEN = LogPattern(r'-', None)


