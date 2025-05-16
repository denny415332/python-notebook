from functools import wraps
from time import sleep
from typing import Callable, Any


def retry_on_error(
    run_func_when_error: Callable[..., Any] | None = None,
    max_retries: int = 3,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """當發生錯誤時重試的裝飾器

    Args:
        run_func_when_error (Callable[..., Any] | None, optional): 當發生錯誤時要執行的函數
        max_retries (int, optional): 問題處理的最大重試次數. 預設為 3.
    """

    def decorator(decorated_function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(decorated_function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            main_attempt = 0
            max_main_attempts = max_retries + 1

            # 如果沒有提供要執行的函數，則直接執行主函式
            if run_func_when_error is None:
                return decorated_function(*args, **kwargs)

            # 如果提供了要執行的函數，則執行主函式，並在發生錯誤時重試
            while main_attempt < max_main_attempts:
                try:
                    print(f"DEBUG - 執行主函式，嘗試次數: {main_attempt + 1}/{max_main_attempts}")
                    return decorated_function(*args, **kwargs)
                except Exception as e:
                    print(f"錯誤: {e}")
                    print("DEBUG - 開始執行錯誤處理函數")

                    # 嘗試執行問題處理（最多重試 max_retries 次）
                    problem_solved = False
                    for retry in range(max_retries + 1):
                        print(f"DEBUG - 執行錯誤處理函數: {run_func_when_error.__name__}")
                        try:
                            run_func_when_error(*args, **kwargs)
                            problem_solved = True
                            print("DEBUG - 錯誤處理函數執行成功")
                            break
                        except Exception as inner_e:
                            print(f"錯誤處理失敗: {inner_e}")
                            if retry < max_retries:
                                print(f"DEBUG - 重試 {retry + 1}/{max_retries}")
                                print("DEBUG - 等待 1 秒後重試")
                                sleep(1)

                    # 如果所有問題處理都失敗，則拋出錯誤
                    if not problem_solved:
                        print("DEBUG - 所有錯誤處理重試都失敗")
                        raise

                    # 主流程重試
                    main_attempt += 1
                    if main_attempt >= max_main_attempts:
                        print("DEBUG - 達到最大重試次數")
                        raise

                    print("DEBUG - 等待 1 秒後重試主函式")
                    sleep(1)

        return wrapper

    return decorator 