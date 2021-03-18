# Standard libraries
import logging
import sys
from typing import (
    IO,
)

# Third party libraries
import bugsnag
from bugsnag.handlers import BugsnagHandler

# Local libraries

def configure(**kargs) -> None:
    bugsnag.configure(
        api_key='13748c4b5f6807a89f327c0f54fe6c7a',
        **kargs
    )


def get_log(
    name: str,
    min_lvl: int = logging.INFO,
    min_bug_lvl: int = logging.ERROR,
    target_file: IO[str] = sys.stderr,
    debug: bool = False
) -> logging.Logger:
    if debug and min_lvl > logging.DEBUG:
        min_lvl = logging.DEBUG
    logger_format: str = '[%(levelname)s] %(message)s'
    logger_formatter: logging.Formatter = logging.Formatter(logger_format)

    logger_handler: logging.Handler = logging.StreamHandler(target_file)
    logger_handler.setFormatter(logger_formatter)

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(min_lvl)
    logger.addHandler(logger_handler)

    bug_handler = BugsnagHandler()
    bug_handler.setLevel(min_bug_lvl)
    logger.addHandler(bug_handler)
    return logger
