from __future__ import annotations
import threading
import time
import random


class BlazeSimulator:
    """模擬 Blaze 裝置"""

    _instance: BlazeSimulator | None = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._temp = 25.0
        self._temp_lock = threading.Lock()

    def get_temp(self) -> float:
        """模擬讀取溫度，加入隨機延遲"""
        with self._temp_lock:
            time.sleep(random.uniform(0.1, 0.3))  # 模擬讀取時間
            self._temp += random.uniform(-0.1, 0.1)  # 模擬溫度變化
            return round(self._temp, 2)


def status_check_thread():
    """狀態檢查執行緒"""
    blaze = BlazeSimulator()
    while True:
        try:
            temp = blaze.get_temp()
            print(f"Status Check: Temperature = {temp}°C")
            time.sleep(0.5)  # 每0.5秒檢查一次
        except KeyboardInterrupt:
            break


def measure_thread():
    """量測執行緒"""
    blaze = BlazeSimulator()
    for i in range(30):  # 模擬30次量測
        try:
            temp = blaze.get_temp()
            print(f"Measure {i + 1}: Temperature = {temp}°C")
            time.sleep(1)  # 模擬量測間隔
        except KeyboardInterrupt:
            break


def main():
    # 建立執行緒
    status_thread = threading.Thread(
        target=status_check_thread, daemon=True, name="StatusCheck"
    )
    measure_thread_obj = threading.Thread(
        target=measure_thread, daemon=True, name="Measure"
    )

    try:
        # 啟動執行緒
        print("Starting threads...")
        status_thread.start()
        measure_thread_obj.start()

        # 等待量測執行緒完成
        measure_thread_obj.join()

        print("\nMeasurement completed!")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        print("Program ended")


if __name__ == "__main__":
    main()
