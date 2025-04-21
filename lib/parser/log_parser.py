from lib.models.constants.log_parser_type import LogParserType
from lib.models.log.echo_log import EchoLog


class LogParser:
    @staticmethod
    def parse_echo_log(host, line):
        if not line:
            return None

        echo_log = EchoLog(host, line)
        if not echo_log.parse_log():
            print("cannot parse log : %s" % line)
            return None

        return echo_log

    def parse_log(self, parser_name, host, line):
        if not line:
            return None

        chunk = line.split(':', 1)
        if len(chunk) < 2:
            print("cannot find : from line %s" % line)
            return None

        path = (chunk[0]).strip()

        parser_tabs = {
            LogParserType.ECHO: {
                '/vagrant/': self.parse_echo_log
            }
        }
        parser_tab = parser_tabs[parser_name]
        if not parser_tab:
            print("cannot find parser : group=%s" % parser_name)
            return None

        parser = None
        for k, v in parser_tab.items():
            if k in path:
                parser = v
                break

        if not parser:
            print("cannot find parser : path=%s" % path)
            return None

        return parser(host, line)
