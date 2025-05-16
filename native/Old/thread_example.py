import threading
import time

# 全局事件對象來控制線程停止
terminate_event = threading.Event()


def start_thread():
    def worker():
        while not terminate_event.is_set():
            print("線程正在工作...")
            time.sleep(1)

    # 創建並啟動線程
    thread = threading.Thread(target=worker)
    thread.start()
    return thread


# 在函式外部創建線程
thread = start_thread()

# 模擬一些處理時間
time.sleep(5)

# 在函式外部停止線程
terminate_event.set()

# 等待線程結束
thread.join()
print("線程已終止。")
