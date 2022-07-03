import os
import sys
import unittest
from pathlib import Path

from loguru import logger

from root import PROJECT_ROOT_PATH

logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    Test_ROOT = f"{PROJECT_ROOT_PATH}/testcase"
    for p in os.listdir(Test_ROOT):
        prev = Path(Test_ROOT).joinpath(p)
        if prev.is_dir() and not p.startswith("__"):
            discover = unittest.TestLoader().discover(str(prev), "test*.py")
            result = runner.run(discover)
            if len(result.errors) > 0:
                logger.info("FIND ERROR!")
                raise Exception("GET ERROR!")
                break
