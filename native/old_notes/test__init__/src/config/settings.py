"""
設置模組 - 提供默認配置
"""

# 默認配置
DEFAULT_CONFIG = {
    'app_name': '示例應用',
    'debug': False,
    'timeout': 30,
    'database': {
        'host': 'localhost',
        'port': 5432,
        'user': 'admin',
        'password': 'secret'
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
} 