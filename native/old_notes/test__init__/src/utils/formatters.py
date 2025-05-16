"""
格式化工具模組 - 提供格式化功能
"""

def format_message(message: str) -> str:
    """格式化訊息"""
    return f"[INFO] {message}"

def format_number(number: float, precision: int = 2) -> str:
    """格式化數字"""
    return f"{number:.{precision}f}"

def calculate_sum(numbers: list) -> float:
    """計算數字列表的總和"""
    return sum(numbers) 