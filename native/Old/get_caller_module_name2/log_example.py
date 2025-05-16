import logging
import inspect


class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def get_caller_module_name(self):
        """獲取呼叫者模組名稱"""

        print("inspect.stack():")
        for frame in inspect.stack():
            module = inspect.getmodule(frame[0])
            print(f"\t{module.__name__ if module else '__unknown__'}")

        # 取得呼叫者模組名稱
        frame = inspect.stack()[2]  # [2] 表示 info() 的呼叫者
        module = inspect.getmodule(frame[0])
        return module.__name__ if module else "__unknown__"

    def info(self, msg):
        module_name = self.get_caller_module_name()
        logging.info(f"[{module_name}] {msg}")


logger = Logger()
