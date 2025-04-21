import logging

logging.basicConfig(level=logging.DEBUG)

import logging

from fabric import Connection

from lib.fabric.fab_ssh_shell import FabSshShell
from lib.fabric.log.ssh_log_shell import SshLogShell
from lib.util.encoding_util import decrypt_cipher_text

logging.basicConfig(level=logging.DEBUG)


class FabSshLogShell(FabSshShell):
    def __init__(self, lock, scheduler, fab_connect_info):
        super().__init__(lock, scheduler, fab_connect_info)
        self.ssh_log_shell = None

    def get_debug_log(self, sub_step, keyword):
        return self.ssh_log_shell.grep_keyword_in_dir_path(keyword, sub_step.value)

    def get_info_log(self, sub_step, keyword):
        file_path = sub_step.value.format(year=self.scheduler.request_id.year,
                                          month=self.scheduler.request_id.month,
                                          day=self.scheduler.request_id.day)
        return self.ssh_log_shell.grep_keyword_in_file_path(keyword, file_path)

    def get_search_log(self, proc_id, return_dict, keyword):
        log = None

        # paramiko 로그 메시지 줄이기
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("invoke").setLevel(logging.WARNING)
        logging.getLogger("fabric").setLevel(logging.WARNING)

        if self.fab_connect_info.gateway_host is not None:
            gateway = Connection(
                host=self.fab_connect_info.gateway_host,
                user=self.fab_connect_info.gateway_user,
                connect_kwargs={"password": decrypt_cipher_text(self.fab_connect_info.gateway_password)},
                # 또는 key_filename 사용 가능
            )

            # 최종 목적지 서버 설정 (게이트웨이를 통해 접속)
            fab_connect = Connection(
                host=self.fab_connect_info.host,
                user=self.fab_connect_info.user,
                connect_kwargs={"password": decrypt_cipher_text(self.fab_connect_info.password)},
                gateway=gateway
            )
        else:
            fab_connect = Connection(
                host=self.fab_connect_info.host,
                user=self.fab_connect_info.user,
                connect_kwargs={"password": decrypt_cipher_text(self.fab_connect_info.password)},
            )

        self.ssh_log_shell = SshLogShell(self.lock, self.scheduler, fab_connect)

        current_main_step = self.scheduler.get_current_main_step()
        if current_main_step is None:
            return return_dict

        log = self.ssh_log_shell.grep_keyword_in_file_path(keyword, current_main_step.value)

        # if log is None:
        #     log = ""

        return_dict[proc_id] = log

