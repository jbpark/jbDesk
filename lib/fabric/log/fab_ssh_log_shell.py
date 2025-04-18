import logging

from lib.fabric.fab_ssh_shell import FabSshShell
from lib.models.constants.log_step import LogStepSearch

logging.basicConfig(level=logging.DEBUG)

import logging
from symbol import and_expr

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

    # def get_search_log_rest(self, keyword):
    #     all_sub_steps = self.scheduler.get_all_sub_steps()
    #     for sub_step in all_sub_steps:
    #         if sub_step == TrLogSubStepRestApi.REST_DEBUG_LOG:
    #             log = self.get_debug_log(sub_step, keyword)
    #             if log:
    #                 return log
    #         elif sub_step == TrLogSubStepRestApi.REST_INFO_LOG:
    #             log = self.get_info_log(sub_step, keyword)
    #             if log:
    #                 return log
    #
    # def get_gaetway_access_log(self, sub_step, keyword):
    #     return self.ssh_log_shell.grep_first_keyword_in_dir_path(keyword, sub_step.value)
    #
    # def get_search_log_gateway_api(self, keyword):
    #     main_step = self.scheduler.get_current_main_step
    #     all_sub_steps = self.scheduler.get_all_sub_steps()
    #     for sub_step in all_sub_steps:
    #         if sub_step == TrLogSubStepGatewayApi.GATEWAY_ACCESS_LOG:
    #             log = self.get_gaetway_access_log(sub_step, keyword)
    #             if log:
    #                 return log
    #
    # def get_search_log_api_service(self, keyword):
    #     main_step = self.scheduler.get_current_main_step
    #     if self.scheduler.year is not None and \
    #         self.scheduler.month is not None and \
    #         self.scheduler.day is not None:
    #         file_path = TrLogSubStepGatewayApi.API_ACCESS_FILE_LOG.value.format(
    #             name=self.scheduler.api_service_name,
    #             year=self.scheduler.year,
    #             month=self.scheduler.month,
    #             day=self.scheduler.day
    #         )
    #         access_log = self.ssh_log_shell.grep_keyword_in_file_path(keyword, file_path)
    #     else:
    #         file_path = TrLogSubStepGatewayApi.API_ACCESS_ALL_LOG.value.format(
    #             name=self.scheduler.api_service_name
    #         )
    #         access_log = self.ssh_log_shell.grep_keyword_in_file_path(keyword, file_path)
    #
    #     dir_path = TrLogSubStepGatewayApi.API_DEBUG_LOG.value.format(
    #         name=self.scheduler.api_service_name
    #     )
    #     debug_log = self.ssh_log_shell.grep_keyword_in_dir_path(keyword, dir_path)
    #
    #     if debug_log:
    #         if access_log:
    #             return access_log + '\n' + debug_log
    #         else:
    #             return debug_log
    #
    #     file_path = TrLogSubStepGatewayApi.API_INFO_LOG.value.format(
    #         name=self.scheduler.api_service_name,
    #         year=self.scheduler.year,
    #         month=self.scheduler.month,
    #         day=self.scheduler.day
    #     )
    #     info_log = self.ssh_log_shell.grep_keyword_in_dir_path(keyword, file_path)
    #     if access_log:
    #         return access_log + '\n' + info_log
    #     else:
    #         return info_log

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

        if current_main_step == LogStepSearch.GATEWAY:
            log = self.ssh_log_shell.grep_keyword_in_file_path(keyword, current_main_step.value)
        #     log = self.get_search_log_rest(keyword)
        # elif current_main_step == TrLogStepMiddleware.INFRA_GATEWAY_API:
        #     log = self.get_search_log_gateway_api(keyword)
        # elif current_main_step == TrLogStepMiddleware.API_SERVICE:
        #     log = self.get_search_log_api_service(keyword)

        if log is None:
            return_dict[proc_id] = log

