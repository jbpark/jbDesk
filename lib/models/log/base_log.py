import re

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

class BaseLog:
    def __init__(self, host, log):
        self.host = host
        self.log = log
        self.file = None
        self.local_date = None
        self.pattern_group = None

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

    def parse_log(self):
        result = False
        for pattern_list in self.pattern_group:
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

        if not result:
            print("cannot find parser : %s" % self.log)

        return result

    def get_display_log(self):
        result = DisplayLog(self.host)
        result.path = self.file
        return result
