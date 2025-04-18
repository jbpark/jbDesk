from multiprocessing import Manager

g_process_manager = None
g_shared_list = None

def set_process_manager():
    global g_process_manager
    global g_shared_list
    g_process_manager = Manager()
    g_shared_list = g_process_manager.list()

def get_process_manager():
    return g_process_manager

def get_shared_list():
    return g_shared_list