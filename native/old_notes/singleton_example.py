class Singleton:
    # 類屬性
    _instance = None
    class_counter = 0  # 用於追蹤實例化次數
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.class_counter += 1  # 增加計數器
        return cls._instance
    
    def __init__(self):
        # 實例屬性
        if not hasattr(self, 'initialized'):
            self.instance_counter = 0  # 實例計數器
            self.initialized = True
    
    def increment_instance_counter(self):
        self.instance_counter += 1
        return self.instance_counter
    
    @classmethod
    def get_class_counter(cls):
        return cls.class_counter

# 使用示例
if __name__ == "__main__":
    # 創建第一個實例
    singleton1 = Singleton()
    print(f"類計數器: {Singleton.get_class_counter()}")  # 應該顯示 1
    print(f"實例1計數器: {singleton1.instance_counter}")  # 應該顯示 0
    
    # 增加實例1的計數器
    singleton1.increment_instance_counter()
    print(f"實例1計數器: {singleton1.instance_counter}")  # 應該顯示 1
    
    # 創建第二個實例（實際上是同一個實例）
    singleton2 = Singleton()
    print(f"類計數器: {Singleton.get_class_counter()}")  # 應該顯示 1
    print(f"實例2計數器: {singleton2.instance_counter}")  # 應該顯示 1
    
    # 增加實例2的計數器
    singleton2.increment_instance_counter()
    print(f"實例2計數器: {singleton2.instance_counter}")  # 應該顯示 2
    print(f"實例1計數器: {singleton1.instance_counter}")  # 應該顯示 2 