from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "2.0.1"

_conf = BugsnagConf(
    "service", __version__, "./observes/service/batch-stability", False
)
set_bugsnag(_conf)
LOG = set_main_log(__name__)
