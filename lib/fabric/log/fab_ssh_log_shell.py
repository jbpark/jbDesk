import logging

from lib.fabric.fab_ssh_shell import FabSshShell

logging.basicConfig(level=logging.DEBUG)


class FabSshLogShell(FabSshShell):
    def __init__(self, lock, scheduler, fab_connect_info):
        super().__init__(lock, scheduler, fab_connect_info)

    def find_file_date(self, keyword):
        print("")

    def get_search_log(self, proc_id, return_dict, group_name, service_name,
                       level, keyword, log_paths):
        log = None

        # paramiko 로그 메시지 줄이기
        logging.getLogger("paramiko").setLevel(logging.WARNING)

