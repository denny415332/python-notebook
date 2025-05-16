from simple_retry_decorator import retry_on_error


def error_handler():
    """錯誤處理函數 - 總是成功"""
    print("DEBUG - 執行錯誤處理函數")
    # 模擬錯誤處理成功
    return True


def failing_error_handler():
    """錯誤處理函數 - 總是失敗"""
    print("DEBUG - 執行錯誤處理函數（失敗版本）")
    # 模擬錯誤處理失敗
    raise Exception("錯誤處理失敗")


@retry_on_error(run_func_when_error=error_handler, max_retries=2)
def main_function(value: int) -> int:
    """主函數，模擬可能發生錯誤的操作"""
    print(f"DEBUG - 主函數執行，輸入值: {value}")
    if value < 0:
        raise Exception("數值不能為負數")
    return value * 2


@retry_on_error(run_func_when_error=failing_error_handler, max_retries=2)
def main_function_with_failing_handler(value: int) -> int:
    """主函數，使用會失敗的錯誤處理函數"""
    print(f"DEBUG - 主函數執行（失敗版本），輸入值: {value}")
    if value < 0:
        raise Exception("數值不能為負數")
    return value * 2


if __name__ == "__main__":
    # 測試案例 1：正常情況
    print("\n測試案例 1：正常情況")
    try:
        result = main_function(5)
        print(f"結果: {result}")
    except Exception as e:
        print(f"最終錯誤: {e}")

    # 測試案例 2：錯誤情況（錯誤處理成功）
    print("\n測試案例 2：錯誤情況（錯誤處理成功）")
    try:
        result = main_function(-1)
        print(f"結果: {result}")
    except Exception as e:
        print(f"最終錯誤: {e}")

    # 測試案例 3：錯誤情況（錯誤處理失敗）
    print("\n測試案例 3：錯誤情況（錯誤處理失敗）")
    try:
        result = main_function_with_failing_handler(-1)
        print(f"結果: {result}")
    except Exception as e:
        print(f"最終錯誤: {e}") 