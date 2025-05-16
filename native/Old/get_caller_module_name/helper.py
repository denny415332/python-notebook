import inspect


def get_caller_module_name() -> str | None:
    """獲取呼叫者模組名稱

    Returns:
        str: 呼叫者模組名稱
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if module:
        return module.__name__
    return None
