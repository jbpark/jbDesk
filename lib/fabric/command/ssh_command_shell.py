from lib.fabric.ssh_shell import SshShell


class SshCommandShell(SshShell):
    def __init__(self, lock, scheduler, fab_connect):
        super().__init__(lock, scheduler, fab_connect)

    def get_os_info(self):
        res = self.fab_connect.sudo('rpm -qa *-release', shell=False)
        os_info = {}
        if res.find('centos-release-') == -1:
            print('OS Version : Not Found')
        else:
            os_info["name"] = "centos"
            for line in res.splitlines():
                line = line.strip()
                if line.find('centos-release-') == -1:
                    continue

                items = line.split('.')
                os_string = items[0]
                os_version = os_string[15:]
                os_version = os_version.replace("-", ".")
                os_info["version"] = os_version

        return os_info
