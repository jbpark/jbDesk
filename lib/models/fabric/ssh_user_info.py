class SshUserInfo:
    def __init__(self, index, user_name, password):
        self.index = index
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return f"SshUserInfo(index='{self.index}', user_name='{self.user_name}', password='{self.password}')"
