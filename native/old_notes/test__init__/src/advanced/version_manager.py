"""
版本管理器模組 - 提供版本管理功能
"""

from packaging import version

class VersionManager:
    """版本管理器"""
    def __init__(self, current_version: str):
        self.current_version = current_version

    def check_version(self, required_version: str) -> bool:
        """檢查版本是否滿足要求"""
        return version.parse(self.current_version) >= version.parse(required_version)

    def get_version_info(self) -> dict:
        """獲取版本信息"""
        return {
            'current_version': self.current_version,
            'major': version.parse(self.current_version).major,
            'minor': version.parse(self.current_version).minor,
            'patch': version.parse(self.current_version).micro
        }

def check_version(current_version: str, required_version: str) -> bool:
    """檢查版本是否滿足要求"""
    return VersionManager(current_version).check_version(required_version) 