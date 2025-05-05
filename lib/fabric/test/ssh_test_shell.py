from lib.fabric.ssh_shell import SshShell


class SshTestShell(SshShell):
    def __init__(self, lock, scheduler, fab_connect):
        super().__init__(lock, scheduler, fab_connect)

    def get_os_info(self):
        try:
            conn = self.fab_connect

            # 먼저 /etc/os-release 파일이 있는지 확인
            if conn.run("test -f /etc/os-release", warn=True, hide=True).ok:
                result = conn.sudo("cat /etc/os-release", hide=True)
                lines = result.stdout.strip().split('\n')

                os_info = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os_info[key] = value.strip('"')

                os_name = os_info.get("NAME", "Unknown")
                os_version = os_info.get("VERSION_ID", "Unknown")
                return f"{os_name} {os_version}"

            # fallback: /etc/redhat-release (CentOS 6 등)
            elif conn.run("test -f /etc/redhat-release", warn=True, hide=True).ok:
                result = conn.sudo("cat /etc/redhat-release", hide=True)
                output = result.stdout.strip()

                # 예: "CentOS release 6.10 (Final)"
                if output.startswith("CentOS"):
                    parts = output.split()
                    os_name = parts[0]
                    os_version = parts[2]
                else:
                    os_name = "Unknown"
                    os_version = "Unknown"
                return f"{os_name} {os_version}"

            else:
                return "Unknown Unknown"

        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

