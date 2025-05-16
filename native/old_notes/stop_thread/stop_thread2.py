from threading import Thread
import ctypes
import time

# 創建一個全局變量來控制線程
should_stop = False


def force_stop_thread(thread):
    """強制停止線程的函數"""
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        thread_id, ctypes.py_object(SystemExit)
    )
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print("Failed to stop thread")


def fun(*args):
    print(*args)
    if should_stop:
        raise SystemExit
    time.sleep(1)


def test_thread():
    try:
        for i in range(1000):
            if should_stop:
                print("Thread stopping...")
                break
            fun(i)
            fun(i, i)
            fun(i, i, i)
            fun(i, i, i, i)
            fun(i, i, i, i, i)
    except SystemExit:
        print("Thread forcefully stopped!")


thread = Thread(target=test_thread, daemon=True)
thread.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt - Force stopping thread...")
        # global should_stop
        should_stop = True
        # 等待一秒看看線程是否正常停止
        time.sleep(1)
        if thread.is_alive():
            print("Thread still running, forcing stop...")
            force_stop_thread(thread)
        thread.join(timeout=2)
        print("Thread stopped successfully")
        break
