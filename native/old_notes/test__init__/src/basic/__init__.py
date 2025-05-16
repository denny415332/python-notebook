"""
基本範例模組 - 展示 __init__.py 的基本用法
"""

# 版本資訊
__version__ = '0.1.0'

# 定義套件級別的變數
PACKAGE_NAME = 'basic_example'

# 定義可以被外部訪問的函數
def hello():
    """返回一個問候語"""
    return "你好，這是一個基本範例！"

# 定義可以被外部訪問的類別
class ExampleClass:
    """示例類別"""
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"你好，{self.name}！"

# 定義可以被外部訪問的變數
DEFAULT_SETTINGS = {
    'debug': False,
    'timeout': 30
}

# 使用 __all__ 控制 from package import * 時要導入的內容
__all__ = ['hello', 'ExampleClass', 'DEFAULT_SETTINGS']

# 進階功能：定義套件級別的異常
class PackageError(Exception):
    """套件自定義異常"""
    pass

# 進階功能：套件初始化時的設置
def _setup():
    """套件初始化設置"""
    import logging
    logging.basicConfig(level=logging.INFO)
    return True

# 執行初始化
_setup()

# 進階功能：提供版本檢查
def check_version(required_version: str) -> bool:
    """檢查版本是否滿足要求"""
    from packaging import version
    return version.parse(__version__) >= version.parse(required_version) 