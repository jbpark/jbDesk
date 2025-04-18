def lock_print(lock, message):
    lock.acquire()
    try:
        print(message)
    finally:
        lock.release()
    return
