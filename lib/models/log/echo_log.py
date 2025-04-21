from lib.models.constants.reg_pattern import RegPattern
from lib.models.log.base_log import BaseLog
from lib.models.log.log_pattern import LogPattern
from lib.util.date_util import DateUtil


class EchoLog(BaseLog):

    def __init__(self, host, log):
        super().__init__(host, log)
        self.date, self.level = None, None
        self.class_name = None
        self.message = None
        self.trace_id = None
        self.span_id = None
        self.parent_span_id = None
        self.resource = None
        self.status_code = None
        self.request_id = None
        # pattern
        self.pattern_group = [
            [
                LogPattern(RegPattern.WORD, self.set_file), RegPattern.COLON,
                LogPattern(RegPattern.TIMESTAMP, self.set_date), RegPattern.SPACE,
                LogPattern(RegPattern.WORD, self.set_level), RegPattern.SPACE_MORE,
                LogPattern(RegPattern.ANY, self.set_message)
            ]
        ]

    def set_date(self, date):
        self.date = date
        self.local_date = DateUtil.convert_datetime_timezone(date, DateUtil.TIME_ZONE_US_PACIFIC,
                                                             DateUtil.TIME_ZONE_LOCAL)

    def set_level(self, level):
        self.level = self.extract_log_level(level)

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_message(self, message):
        self.message = message

        # class name 이 com.trumpia.api.service.RemoteLogService 인 경우
        if self.class_name == 'com.trumpia.api.service.RemoteLogService':
            self.resource = self.find_pattern(RegPattern.RESOURCE, message)
            print('resource=%s' % self.resource)
            self.status_code = self.find_pattern(RegPattern.STATUS_CODE, message)
            print('status_code=%s' % self.status_code)
            self.request_id = self.find_pattern(RegPattern.REQUEST_ID, message)
            print('request_id=%s' % self.request_id)

    def set_trace_span_parent_id(self, id_str):
        id_array = id_str.split(',')
        self.trace_id = id_array[0]
        self.span_id = id_array[1] if len(id_str) > 1 else '-'
        self.parent_span_id = id_array[2] if len(id_str) > 2 else '-'

    def get_display_log(self):
        result = super(EchoLog, self).get_display_log()
        result.date = self.date
        result.level = self.level
        result.trace_id = '-'
        result.span_id = '-'
        result.parent_span_id = '-'
        result.message = self.message

        return result

def parse_log_test():
    log = "/home/vagrant/gateway.log:2025-04-08 11:01:10,280 [INFO] TID=db34a6fa-af3d-4aad-a783-6fbbb4b2bf65: Incoming request"
    echo_log = EchoLog("localhost", log)
    echo_log.parse_log()
    display_log = echo_log.get_display_log()
    print(f"{display_log}")


if __name__ == "__main__":
    parse_log_test()