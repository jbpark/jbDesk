import sys

from lib.fabric.ssh_shell import SshShell
from lib.util.process_util import lock_print

# 실행할 셸 명령어 (쉘 루프를 문자열로 직접 작성)
shell_cmd_find_first = '''
for file in $(ls -t {dir_path}); do
    if grep -q "{keyword}" "$file"; then
        grep --with-filename -m1 "{keyword}" "$file"
        break
    fi
done
'''


class SshLogShell(SshShell):
    def __init__(self, lock, scheduler, fab_connect):
        super().__init__(lock, scheduler, fab_connect)

    def grep_keyword_in_dir_path(self, keyword, dir_path):
        try:
            res = self.fab_connect.run("grep -r \'%s\' %s" % (keyword, dir_path), hide=True, warn=True)
            if res.exited != 0:
                lock_print(self.lock, 'No matches found or error occurred:' + res.stderr)
                log = None
            else:
                lock_print(self.lock, res.stdout)
                log = res.stdout
        except:
            lock_print(self.lock, sys.exc_info()[0])
            log = None

        return log

    def grep_keyword_in_file_path(self, keyword, file_path):
        try:
            res = self.fab_connect.run("grep --with-filename \'%s\' %s" % (keyword, file_path), hide=True, warn=True)
            if res.exited != 0:
                lock_print(self.lock, 'No matches found or error occurred:' + res.stderr)
                log = None
            else:
                lock_print(self.lock, res.stdout)
                log = res.stdout
        except:
            lock_print(self.lock, sys.exc_info()[0])
            log = None

        return log

    def grep_first_keyword_in_dir_path(self, keyword, dir_path):
        try:
            res = self.fab_connect.run(shell_cmd_find_first.format(keyword=keyword, dir_path=dir_path),
                                       hide=True, warn=True)
            if res.exited != 0:
                lock_print(self.lock, 'No matches found or error occurred:' + res.stderr)
                log = None
            else:
                lock_print(self.lock, res.stdout)
                log = res.stdout
        except:
            lock_print(self.lock, sys.exc_info()[0])
            log = None

        return log

