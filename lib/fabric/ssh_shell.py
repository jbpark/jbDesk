
class SshShell:
    def __init__(self, lock, scheduler, fab_connect):
        self.lock = lock
        self.scheduler = scheduler
        self.fab_connect = fab_connect
