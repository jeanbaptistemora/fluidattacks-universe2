import bugsnag
from bugsnag.handlers import (
    BugsnagHandler,
)
import logging
from os import (
    environ,
)
import sys
from typing import (
    Any,
    IO,
)

ENV = environ.get("OBSERVES_ENV", "production")
DEBUG = environ.get("OBSERVES_DEBUG", "false").lower() == "true"


def configure(**kargs: Any) -> None:
    bugsnag.configure(
        api_key="13748c4b5f6807a89f327c0f54fe6c7a", release_stage=ENV, **kargs
    )


def main_log(
    name: str,
    min_lvl: int = logging.INFO,
    min_bug_lvl: int = logging.ERROR,
    target_file: IO[str] = sys.stderr,
    debug: bool = DEBUG,
) -> logging.Logger:
    if debug and min_lvl > logging.DEBUG:
        min_lvl = logging.DEBUG
    prefix = "%(name)s> " if debug else ""
    logger_format: str = prefix + "[%(levelname)s] %(message)s"
    logger_formatter: logging.Formatter = logging.Formatter(logger_format)

    logger_handler: logging.Handler = logging.StreamHandler(target_file)
    logger_handler.setFormatter(logger_formatter)

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(min_lvl)
    logger.addHandler(logger_handler)
    if not debug:
        bug_handler = BugsnagHandler()
        bug_handler.setLevel(min_bug_lvl)
        logger.addHandler(bug_handler)
    logger.info("%s env: %s", name, ENV)
    return logger
