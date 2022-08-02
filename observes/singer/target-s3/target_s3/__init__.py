from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "0.2.0"

_conf = BugsnagConf(
    "target", __version__, "./observes/singer/target_s3", False
)
set_bugsnag(_conf)
LOG = set_main_log(__name__)
