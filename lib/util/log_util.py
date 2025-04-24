import re
from datetime import datetime

import pytz

DATE_PATTERNS = [
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3}', '%Y-%m-%d %H:%M:%S %Z'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '%Y-%m-%d %H:%M:%S'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', '%Y-%m-%d %H:%M'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M:%S %p'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M %p'),
    (r'\d{4}-\d{1,2}-\d{1,2} [APap][Mm] \d{1,2}:\d{1,2}:\d{1,2}', '%Y-%m-%d %p %I:%M:%S'),
    (r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%Y-%m-%d %I:%M:%S %p'),
    (r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [-+]\d{4}', '%d/%b/%Y:%H:%M:%S %z')
]

def convert_log_timezone(log_text: str, source_timezone: str, dest_timezone: str) -> str:
    already_converted = []

    for pattern, date_format in DATE_PATTERNS:
        def replace_fn(match):
            datetime_str = match.group(0)

            # 중복 방지: 이미 변환된 문자열이면 건너뛴다
            if match.start() in already_converted:
                return datetime_str

            try:
                dt = datetime.strptime(datetime_str, date_format)
                if '%z' not in date_format and '%Z' not in date_format:
                    source_tz = pytz.timezone(source_timezone)
                    dt = source_tz.localize(dt)
                dt = dt.astimezone(pytz.timezone(dest_timezone))
                new_datetime_str = dt.strftime(date_format)

                # 이 위치는 처리했음 표시
                already_converted.append(match.start())

                return new_datetime_str
            except Exception:
                return datetime_str  # 오류 발생 시 원래 문자열 유지

        log_text = re.sub(pattern, replace_fn, log_text)

    return log_text


def convert_log_timezone_line(log_text: str, source_timezone: str, dest_timezone: str):
    lines = log_text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([convert_log_timezone(line, source_timezone, dest_timezone) for line in lines])
