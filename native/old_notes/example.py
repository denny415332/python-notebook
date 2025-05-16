class Example:
    # 類屬性
    class_param = "這是類屬性"
    
    def __init__(self):
        # 實例屬性
        self.instance_param = "這是實例屬性"
    
    def instance_method(self):
        # 使用實例屬性
        print(f"實例方法中的實例屬性: {self.instance_param}")
        # 也可以訪問類屬性
        print(f"實例方法中的類屬性: {self.class_param}")
    
    @classmethod
    def class_method(cls):
        # 使用類屬性
        print(f"類方法中的類屬性: {cls.class_param}")
        # 不能直接訪問實例屬性
        # print(cls.instance_param)  # 這會報錯

# 使用示例
if __name__ == "__main__":
    # 創建實例
    obj1 = Example()
    obj2 = Example()
    
    # 修改實例屬性
    obj1.instance_param = "修改後的實例屬性"
    
    # 修改類屬性
    Example.class_param = "修改後的類屬性"
    
    # 調用方法
    print("\n實例 1:")
    obj1.instance_method()
    
    print("\n實例 2:")
    obj2.instance_method()
    
    print("\n類方法:")
    Example.class_method() 