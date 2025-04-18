class SshConnectInfo:
    def __init__(self, host_ip, ssh_user_info):
        self.host_ip = host_ip
        self.ssh_user_info = ssh_user_info

    def __repr__(self):
        return f"SshConnectInfo(host_ip={self.host_ip}, ssh_user_info='{self.ssh_user_info}')"
