from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "2.0.0"

_conf = BugsnagConf("tap", __version__, "./observes/singer/tap_checkly", False)
set_bugsnag(_conf)
LOG = set_main_log(__name__)
