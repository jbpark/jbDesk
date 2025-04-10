import re
import time
from datetime import datetime

import pytz


class DateUtil:
    TIME_ZONE_US_PACIFIC = 'US/Pacific'
    TIME_ZONE_ASIA_SEOUL = 'Asia/Seoul'
    TIME_ZONE_LOCAL = TIME_ZONE_ASIA_SEOUL

    # Define a list of date patterns and corresponding format strings
    # "The meeting is scheduled for 2023-10-09 14:30:00 UTC and 10/09/2023 3:45 PM in London."
    # "The meeting is scheduled for 08/Oct/2023:23:13:24 -0700"
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

    @staticmethod
    def convert_datetime_timezone(text, tz_src, tz_dst):
        source_timezone = pytz.timezone(tz_src)
        target_timezone = pytz.timezone(tz_dst)

        text = text.replace("오후", "PM")
        text = text.replace("오전", "AM")
        text = text.replace("  ", " ")

        # Loop through the date patterns and replace time zones
        for date_pattern, format_string in DateUtil.DATE_PATTERNS:
            # Find all date-time strings for the current pattern
            date_strings = re.findall(date_pattern, text)

            # Loop through the found date-time strings and replace time zones
            for date_string in date_strings:
                # Parse the date-time string to a datetime object in the source time zone
                dt_source = datetime.strptime(date_string, format_string)
                if format_string != '%d/%b/%Y:%H:%M:%S %z':
                    dt_source = source_timezone.localize(dt_source)

                # Convert the datetime object to the target time zone
                dt_target = dt_source.astimezone(target_timezone)

                # Format the datetime back to a string with the new time zone
                new_date_string = dt_target.strftime(format_string)

                # Replace the original date-time string with the new one in the text
                text = text.replace(date_string, new_date_string)

        return text

    @staticmethod
    def convert_ps_start_time(text):
        pattern = r'(\w{3}) (\w{3}) {1,2}(\d{1,2}) (\d{2}:\d{2}:\d{2}) (\d{4})'

        # Use re.search to capture date components
        match = re.search(pattern, text)

        if match:
            day_of_week, month, day, hour_min_sec, year = match.groups()
            # Convert month name to a numeric month
            months = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            numeric_month = months[month]

            pattern = r'\b(\d)\b'
            day = re.sub(pattern, r'0\1', day)

            # Create the new date format
            new_date = f"{year}-{numeric_month}-{day} {hour_min_sec}"
            print(f"Original date: {text}")
            print(f"Changed date: {new_date}")
        else:
            print("No matching date found in the specified format.")
            new_date = ""

        return new_date

    @staticmethod
    def get_elapsed_time_str(start_time):
        elapsed_time = time.time() - start_time
        rounded_time = round(elapsed_time, 2)
        return "{:.2f}".format(rounded_time)

    @staticmethod
    def convert_timestamp_dateformat(timestamp, date_format, time_zone):
        #desired_time_zone = pytz.timezone(time_zone)
        #my_datetime_desired_tz = timestamp.astimezone(desired_time_zone)
        return timestamp.strftime(date_format)

    @staticmethod
    def convert_utc_timestamp_dateformat(timestamp, date_format, time_zone):
        datetime_utc = datetime.utcfromtimestamp(timestamp)

        utc_timezone = pytz.timezone('UTC')
        datetime_utc = utc_timezone.localize(datetime_utc)

        # Convert to Pacific Daylight Time (PDT)
        pdt_timezone = pytz.timezone(time_zone)
        datetime_pdt = datetime_utc.astimezone(pdt_timezone)

        return datetime_pdt.strftime(date_format)

    @staticmethod
    def convert_utc_datetime_dateformat(utc_datetime_str, date_format, time_zone):
        utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%SZ")

        # Set the timezone to UTC
        utc_timezone = pytz.utc
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to Dst Time Zone
        dst_timezone = pytz.timezone(time_zone)
        dst_datetime = utc_datetime.astimezone(dst_timezone)

        return dst_datetime.strftime(date_format)

    @staticmethod
    def get_today_dateformat(date_format, time_zone):
        target_timezone = pytz.timezone(time_zone)  # Replace with your target timezone
        current_datetime = datetime.now(target_timezone)
        return current_datetime.strftime(date_format)

    @staticmethod
    def convert_time_between_two_timezone(source_time_zone, dest_time_zone,
                                          source_time_format, dest_time_format, source_time_str):
        source_timezone = pytz.timezone(source_time_zone)
        source_datetime = datetime.strptime(source_time_str, source_time_format)
        source_datetime = source_timezone.localize(source_datetime)

        # Convert to the destination timezone
        dest_timezone = pytz.timezone(dest_time_zone)
        dest_datetime = source_datetime.astimezone(dest_timezone)

        # Format the result
        return dest_datetime.strftime(dest_time_format)

    @staticmethod
    def convert_date_format(source_date_format, dest_date_format, source_date_str):
        if source_date_str is None:
            return None

        input_date = datetime.strptime(source_date_str, source_date_format)

        return input_date.strftime(dest_date_format)

    @staticmethod
    def is_match_date_format(date_format, datetime_str):
        try:
            datetime.strptime(datetime_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_match_iso8601_date_format(datetime_str):
        return DateUtil.is_match_date_format("%Y-%m-%dT%H:%M:%SZ", datetime_str)

def get_today_dateformat_test():
    source_time_zone = "Asia/Seoul"
    dest_time_zone = "US/Pacific"
    source_time_format = "%m/%d/%Y %H:%M"
    dest_time_format = "%m/%d/%Y %H:%M"
    source_time_str = DateUtil.get_today_dateformat("%m/%d/%Y", "Asia/Seoul") + " 00:00"
    print(f"{source_time_str}")

    result = DateUtil.convert_time_between_two_timezone(source_time_zone, dest_time_zone,
                                                        source_time_format, dest_time_format, source_time_str)
    print(f"{result}")

def convert_utc_datetime_dateformat_test():
    dest_time_zone = "US/Pacific"
    dest_time_format = "%Y-%m-%d %H:%M"
    #utc_datetime_str = "2024-02-11T00:19:16Z"
    utc_datetime_str = "2024-03-10T10:00:00Z"

    if DateUtil.is_match_iso8601_date_format(utc_datetime_str):
        print("is match")
    else:
        print("is not match")

    result = DateUtil.convert_utc_datetime_dateformat(utc_datetime_str, dest_time_format, dest_time_zone)
    print(f"{result}")

if __name__ == "__main__":
    #get_today_dateformat_test()
    convert_utc_datetime_dateformat_test()