"""
示例檔案 - 展示如何使用套件的各種功能
"""

# 導入基本功能
from src.basic import hello, ExampleClass, PackageError

# 導入進階功能
from src.advanced import create_data_processor
from src.config import create_config_manager

# 導入工具函數
from src.utils import format_message, format_number

def demonstrate_basic_features():
    """展示基本功能"""
    print("\n=== 基本功能展示 ===")
    
    # 使用基本函數
    print(hello())  # 輸出：你好，這是一個基本範例！
    
    # 使用類別
    user = ExampleClass("小明")
    print(user.greet())  # 輸出：你好，小明！
    
    # 使用自定義異常
    try:
        raise PackageError("這是一個測試錯誤")
    except PackageError as e:
        print(f"捕獲到錯誤：{e}")

def demonstrate_data_processing():
    """展示數據處理功能"""
    print("\n=== 數據處理功能展示 ===")
    
    # 創建數據處理器
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processor = create_data_processor(numbers)
    
    # 過濾偶數
    even_numbers = processor.filter(lambda x: x % 2 == 0)
    print(f"偶數：{even_numbers}")
    
    # 計算平方
    squares = processor.map(lambda x: x ** 2)
    print(f"平方：{squares}")
    
    # 計算總和
    total = processor.reduce(lambda x, y: x + y)
    print(f"總和：{total}")

def demonstrate_config_management():
    """展示配置管理功能"""
    print("\n=== 配置管理功能展示 ===")
    
    # 創建配置管理器
    config = create_config_manager("app_config.json")
    
    # 設置配置
    config.set("app_name", "我的應用")
    config.set("database", {
        "host": "localhost",
        "port": 5432,
        "user": "admin"
    })
    
    # 讀取配置
    app_name = config.get("app_name")
    db_config = config.get("database")
    print(f"應用名稱：{app_name}")
    print(f"數據庫配置：{db_config}")

def demonstrate_utility_functions():
    """展示工具函數"""
    print("\n=== 工具函數展示 ===")
    
    # 格式化訊息
    message = format_message("系統啟動成功")
    print(message)
    
    # 格式化數字
    pi = 3.14159
    formatted_pi = format_number(pi, 3)
    print(f"圓周率：{formatted_pi}")

def demonstrate_combined_usage():
    """展示組合使用"""
    print("\n=== 組合使用展示 ===")
    
    # 創建配置
    config = create_config_manager("app_config.json")
    config.set("users", ["小明", "小華", "小美"])
    
    # 處理用戶數據
    users = config.get("users", [])
    processor = create_data_processor(users)
    
    # 創建用戶對象
    user_objects = processor.map(lambda name: ExampleClass(name))
    
    # 創建新的處理器來處理用戶對象
    user_processor = create_data_processor(user_objects)
    
    # 獲取問候語
    greetings = user_processor.map(lambda user: user.greet())
    
    # 格式化輸出
    for greeting in greetings:
        print(format_message(greeting))

def main():
    """主函數"""
    print("開始展示套件功能...")
    
    # 展示各種功能
    demonstrate_basic_features()
    demonstrate_data_processing()
    demonstrate_config_management()
    demonstrate_utility_functions()
    demonstrate_combined_usage()
    
    print("\n功能展示完成！")

if __name__ == "__main__":
    main() 