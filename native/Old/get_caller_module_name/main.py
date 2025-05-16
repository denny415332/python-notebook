from helper import get_caller_module_name


def demo():
    print(f"Caller module: {get_caller_module_name()}")


if __name__ == "__main__":
    demo()
