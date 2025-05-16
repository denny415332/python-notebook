from threading import Thread
from time import sleep


def fun_a():
    print("fun_a")
    sleep(100)


def fun_b():
    print("fun_b")
    sleep(100)


def fun_c():
    print("fun_c")
    sleep(100)


global running
running = True


def fun():
    while running:
        fun_a()
        if not running:
            break
        fun_b()
        if not running:
            break
        fun_c()


thread = Thread(target=fun, daemon=True)
thread.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt - Stopping thread...")
        running = False
        thread.join(timeout=3)  # 等待線程最多 3 秒
        if thread.is_alive():
            print("Thread did not stop gracefully, forcing exit...")
        else:
            print("Thread stopped successfully")
        break
