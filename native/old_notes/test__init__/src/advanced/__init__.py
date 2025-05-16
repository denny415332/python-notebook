"""
進階範例模組 - 展示進階功能
"""

from .data_processor import DataProcessor, create_data_processor
from .version_manager import VersionManager, check_version

# 定義可以被外部訪問的內容
__all__ = [
    'DataProcessor',
    'create_data_processor',
    'VersionManager',
    'check_version'
] 