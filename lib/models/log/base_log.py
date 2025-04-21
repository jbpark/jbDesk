import re

from lib.models.constants.reg_pattern import RegPattern
from lib.models.log.log_pattern import LogPattern


class DisplayLog:

    def __init__(self, host):
        self.host = host
        self.path, self.log = None, None
        self.date = None
        self.level = None
        self.trace_id = None
        self.span_id = None
        self.parent_span_id = None
        self.message = None
        self.id = None
        self.class_name = None

    def __str__(self):
        return (
            f"DisplayLog(\n"
            f"  host={self.host},\n"
            f"  path={self.path},\n"
            f"  log={self.log},\n"
            f"  date={self.date},\n"
            f"  level={self.level},\n"
            f"  trace_id={self.trace_id},\n"
            f"  span_id={self.span_id},\n"
            f"  parent_span_id={self.parent_span_id},\n"
            f"  message={self.message},\n"
            f"  id={self.id},\n"
            f"  class_name={self.class_name}\n"
            f")"
        )

class BaseLog:
    def __init__(self, host, log):
        self.host = host
        self.log = log
        self.file = None
        self.local_date = None
        self.pattern_group = None
        self.default_pattern_group = [
            [
                LogPattern(RegPattern.WORD, self.set_file), RegPattern.COLON,
                LogPattern(RegPattern.ANY, self.set_message)
            ]
        ]

    def set_file(self, file):
        self.file = file

    @staticmethod
    def get_pattern_string(pattern):
        result = r'^'
        for item in pattern:
            result += item.pattern

        return result

    @staticmethod
    def find_pattern(pattern, data):
        pattern_name = 'name1'
        match = re.search(pattern % pattern_name, data)
        if not match or not match.group():
            return None

        return match.group(pattern_name)

    @staticmethod
    def find_patterns(pattern, data, *argv):
        result = {}

        match = re.search(pattern % argv, data)
        if not match or not match.group():
            return None

        for arg in argv:
            result[arg] = match.group(arg)

        return result

    def parse_pattern_group(self, pattern_group):
        result = False
        for pattern_list in pattern_group:
            pattern_string = self.get_pattern_string(pattern_list)
            match = re.search(pattern_string, self.log)
            if not match or not match.group():
                continue

            for pattern in pattern_list:
                if not pattern.name:
                    continue

                value = match.group(pattern.name)
                if value:
                    pattern.setter(value)
                    result = True

        return result

    def parse_log(self):
        result = self.parse_pattern_group(self.pattern_group)

        if not result:
            result = self.parse_pattern_group(self.default_pattern_group)

        if not result:
            print("cannot find parser : %s" % self.log)

        return result

    def get_display_log(self):
        result = DisplayLog(self.host)
        result.path = self.file
        return result

    def extract_log_level(self, log_str):
        # 로그 레벨 목록
        levels = ['INFO', 'ERROR', 'WARN', 'TRACE', 'DEBUG', 'FATAL']
        # 정규표현식 패턴 생성 (대소문자 구분 없이 찾기)
        pattern = r'\b(' + '|'.join(levels) + r')\b'
        match = re.search(pattern, log_str, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None