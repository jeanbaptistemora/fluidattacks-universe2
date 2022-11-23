import bugsnag
from logging import (
    ERROR,
    INFO,
    Logger,
)
import sys
from typing import (
    Any,
    IO,
)
from utils_logger.v2 import (
    DEBUG,
    ENV,
    PRODUCT_KEY,
    set_main_log,
)


# type ignores for legacy interface support
def configure(**kargs: Any) -> None:  # type: ignore[misc]
    if not DEBUG:
        bugsnag.configure(  # type: ignore[no-untyped-call]
            api_key=PRODUCT_KEY,
            release_stage=ENV.value,
            **kargs,  # type: ignore[misc]
        )


def main_log(
    name: str,
    min_lvl: int = INFO,
    min_bug_lvl: int = ERROR,
    target_file: IO[str] = sys.stderr,
    debug: bool = DEBUG,
) -> Logger:
    return set_main_log(name, min_lvl, min_bug_lvl, target_file, debug)
