from threading import Thread, Event
from time import sleep

# 創建一個事件對象來控制線程
stop_event = Event()


def fun(*args):
    print(*args)
    sleep(1)


def test_thread():
    for i in range(1000):
        if stop_event.is_set():
            print("Thread stopping...")
            break
        fun(i)
        fun(i, i)
        fun(i, i, i)
        fun(i, i, i, i)
        fun(i, i, i, i, i)


thread = Thread(target=test_thread, daemon=True)
thread.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt - Stopping thread...")
        stop_event.set()  # 設置事件來停止線程
        thread.join()  # 等待線程結束
        print("Thread stopped successfully")
        break
