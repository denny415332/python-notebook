from log_example import logger
from fun import test_function


def test_function_in_main():
    logger.info("從 test_function_in_main 發出的 log")


if __name__ == "__main__":
    test_function()
    test_function_in_main()
