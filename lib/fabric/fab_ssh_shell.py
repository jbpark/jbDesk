class FabSshShell:
    def __init__(self, lock, scheduler, fab_connect_info):
        self.lock = lock
        self.scheduler = scheduler
        self.fab_connect_info = fab_connect_info
