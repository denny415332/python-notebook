import threading
import time
import ctypes
from contextlib import contextmanager


class ForcibleThread(threading.Thread):
    def _get_id(self):
        """取得執行緒ID"""
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                self._thread_id = id
                return id

    def force_stop(self):
        """強制停止執行緒"""
        thread_id = self._get_id()
        if thread_id is not None:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread_id), ctypes.py_object(SystemExit)
            )
            print("執行緒已強制停止" if res == 1 else "強制停止失敗")


class WorkerThread(ForcibleThread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.daemon = True

    def stop(self):
        """正常停止執行緒"""
        self._stop_event.set()

    def stopped(self):
        """檢查是否已停止"""
        return self._stop_event.is_set()

    def run(self):
        """無限循環工作"""
        print("工作執行緒開始運行...")
        try:
            while not self.stopped():
                print("執行緒正在工作...")
                time.sleep(2)  # 模擬工作

        except SystemExit:
            print("執行緒被強制終止")
        except Exception as e:
            print(f"執行緒發生錯誤: {e}")
        finally:
            print("工作執行緒已停止")


class Application:
    @contextmanager
    def worker_context(self):
        self.worker = WorkerThread()
        try:
            self.worker.start()
            yield self.worker
        finally:
            if self.worker.is_alive():
                self.worker.stop()
                time.sleep(1)
                if self.worker.is_alive():
                    self.worker.force_stop()
            print("工作執行緒已清理")

    def run(self):
        with self.worker_context():
            try:
                while True:
                    time.sleep(0.5)
            except Exception as e:
                print(f"錯誤: {e}")


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
