import traceback
import atexit

from src.output.logging_setup import logger


def exit():
    logger.info("Exit")


atexit.register(exit)

try:
    while True:
        pass
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt")
except Exception as e:
    logger.error(f"Error occurred: {e}")
    logger.error(traceback.format_exc())
except BaseException as e:
    logger.error(f"Error occurred: {e}")
    logger.error(traceback.format_exc())
