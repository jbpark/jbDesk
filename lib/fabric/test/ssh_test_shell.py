from lib.fabric.ssh_shell import SshShell


class SshTestShell(SshShell):
    def __init__(self, lock, scheduler, fab_connect):
        super().__init__(lock, scheduler, fab_connect)

    def get_os_info(self):
        # OS 정보 파일 확인
        result = self.fab_connect.sudo("cat /etc/os-release", hide=True)
        lines = result.stdout.strip().split('\n')

        os_info = {}
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                os_info[key] = value.strip('"')

        os_name = os_info.get("NAME", "Unknown")
        os_version = os_info.get("VERSION_ID", "Unknown")

        return f"{os_name} {os_version}"
