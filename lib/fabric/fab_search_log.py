import logging
import sys
import time
from datetime import date, timedelta, datetime, timezone

from fabric.api import run, settings


def lock_print(lock, message):
    lock.acquire()
    try:
        print(message)
    finally:
        lock.release()
    return


def get_find_grep(lock, group_name, service_name, log_path, file_date, keyword):
    log = None
    try:
        # log_path = LogPath()
        # file_path = log_path.get_path(group_name, service_name, level)

        if not file_date:
            file_date = (datetime.now(timezone.utc) + timedelta(-1)).strftime('%Y-%m-%d')

        tm = time.strptime(file_date, '%Y-%m-%d')
        next_tm = date(tm.tm_year, tm.tm_mon, tm.tm_mday) + timedelta(1)
        next_date = next_tm.strftime('%Y-%m-%d')

        find_str = (
            # "for f in $(find %s -name \'*.log\' -o -name \'*.log.*\' -o -name \'*.txt\'); do grep --with-filename \'%s\' $f; done" % (
                "for f in $(find %s -type f -newermt \'%s\' -and ! -newermt \'%s\'); do grep --with-filename \'%s\' $f; done" % (
            log_path, file_date, next_date, keyword))

        print(f"find_str={find_str}")

        res = run(
            # "for f in $(find %s -name \'*.log\' -o -name \'*.log.*\' -o -name \'*.txt\'); do grep --with-filename \'%s\' $f; done" % (
            "for f in $(find %s -type f -newermt \'%s\' -and ! -newermt \'%s\'); do grep --with-filename \'%s\' $f; done" % (
                log_path, file_date, next_date, keyword), shell=False)
        if res.find('No such file') != -1:
            lock_print(lock, 'No such file')
        else:
            lock_print(lock, res)
            log = res
    except:
        lock_print(lock, sys.exc_info()[0])

    return log


def get_search_log(lock, proc_id, return_dict, gateway, host_string, password, in_passwords, group_name, service_name,
                   level, file_date, keyword, log_paths):
    lock_print(lock, host_string)
    log = None

    # paramiko 로그 메시지 줄이기
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    with settings(gateway="%s" % gateway, host_string="%s" % host_string, password="%s" % password,
                  passwords=in_passwords, warn_only=True, timeout=60):
        # with hide('output', 'warnings', 'running'):
        # res = sudo('find %s | xargs grep \"%s\"' % (path, search), shell=False)
        # res = run("for f in %s; do grep --with-filename \'%s\' $f; done" % (path, search), shell=False)
        if len(log_paths) > 1:
            list_log = []
            # list_log.append(get_find_grep(lock, group_name, service_name,
            #                               service_connect_info.get_log_path(LogLevel.ACCESS.value), file_date, keyword))
            # log_debug = get_find_grep(lock, group_name, service_name,
            #                           service_connect_info.get_log_path(LogLevel.DEBUG.value), file_date, keyword)
            # list_log.append(log_debug)
            # if not log_debug:
            #     list_log.append(get_find_grep(lock, group_name, service_name,
            #                                   service_connect_info.get_log_path(LogLevel.INFO.value), file_date, keyword))
            #     list_log.append(get_find_grep(lock, group_name, service_name,
            #                                   service_connect_info.get_log_path(LogLevel.ERROR.value), file_date, keyword))

            for item in list_log:
                if not item:
                    continue

                if not log:
                    log = item
                else:
                    log += '\n' + item
        else:
            log = get_find_grep(lock, group_name, service_name, log_paths[0], file_date, keyword)

    return_dict[proc_id] = log
