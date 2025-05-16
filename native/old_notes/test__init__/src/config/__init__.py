"""
配置管理模組 - 提供配置管理功能
"""

from .config_manager import ConfigManager, create_config_manager
from .settings import DEFAULT_CONFIG

# 定義可以被外部訪問的內容
__all__ = [
    'ConfigManager',
    'create_config_manager',
    'DEFAULT_CONFIG'
] 