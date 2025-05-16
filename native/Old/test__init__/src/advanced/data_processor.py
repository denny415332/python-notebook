"""
數據處理器模組 - 提供數據處理功能
"""

from typing import Any, List, Optional, Dict
from functools import reduce
import json
from pathlib import Path

class DataProcessor:
    """數據處理器"""
    def __init__(self, data: List[Any]):
        self.data = data

    def filter(self, condition: callable) -> List[Any]:
        """過濾數據"""
        return list(filter(condition, self.data))

    def map(self, func: callable) -> List[Any]:
        """映射數據"""
        return list(map(func, self.data))

    def reduce(self, func: callable, initial: Optional[Any] = None) -> Any:
        """歸約數據"""
        if initial is not None:
            return reduce(func, self.data, initial)
        return reduce(func, self.data)

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

def create_data_processor(data: List[Any]) -> DataProcessor:
    """創建數據處理器"""
    return DataProcessor(data)

def create_config_manager(config_path: str) -> ConfigManager:
    """創建配置管理器"""
    return ConfigManager(config_path) 