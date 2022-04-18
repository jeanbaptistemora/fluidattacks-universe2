import bugsnag
from bugsnag.handlers import (
    BugsnagHandler,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
import logging
from logging import (
    Formatter,
    Handler,
    Logger,
)
from os import (
    environ,
)
import sys
from typing import (
    IO,
)


class Envs(Enum):
    PROD = "production"
    DEV = "development"


ENV = Envs(environ.get("OBSERVES_ENV", "production"))
DEBUG = environ.get("OBSERVES_DEBUG", "false").lower() == "true"
PRODUCT_KEY = "13748c4b5f6807a89f327c0f54fe6c7a"  # not a secret


@dataclass(frozen=True)
class BugsnagConf:
    app_type: str
    app_version: str
    project_root: str
    auto_capture_sessions: bool
    api_key: str = PRODUCT_KEY
    release_stage: Envs = ENV


def set_bugsnag(conf: BugsnagConf) -> None:
    if not DEBUG:
        bugsnag.configure(  # type: ignore[no-untyped-call]
            app_type=conf.app_type,
            app_version=conf.app_version,
            project_root=conf.project_root,
            auto_capture_sessions=conf.auto_capture_sessions,
            api_key=conf.api_key,
            release_stage=conf.release_stage.value,
        )


def logger_handler(debug: bool, target: IO[str] = sys.stderr) -> Handler:
    prefix = "%(name)s> " if debug else ""
    _format = prefix + "[%(levelname)s] %(message)s"
    formatter = Formatter(_format)
    handler = logging.StreamHandler(target)
    handler.setFormatter(formatter)
    return handler


def set_main_log(
    name: str,
    min_lvl: int = logging.INFO,
    min_bug_lvl: int = logging.ERROR,
    target: IO[str] = sys.stderr,
    debug: bool = DEBUG,
) -> Logger:
    if debug and min_lvl > logging.DEBUG:
        min_lvl = logging.DEBUG

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(min_lvl)
    logger.addHandler(logger_handler(debug, target))
    if not debug:
        bug_handler = BugsnagHandler()  # type: ignore[no-untyped-call]
        bug_handler.setLevel(min_bug_lvl)
        logger.addHandler(bug_handler)
    logger.info("%s@%s", name, ENV.value)
    return logger


def start_session() -> None:
    bugsnag.start_session()  # type: ignore[no-untyped-call]
