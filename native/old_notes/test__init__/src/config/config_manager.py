"""
配置管理器模組 - 提供配置管理功能
"""

from typing import Any, Dict
import json
from pathlib import Path

class ConfigManager:
    """配置管理器"""
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """載入配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)

    def save_config(self) -> None:
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        """獲取配置值"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """設置配置值"""
        self._config[key] = value
        self.save_config()

def create_config_manager(config_path: str) -> ConfigManager:
    """創建配置管理器"""
    return ConfigManager(config_path) 