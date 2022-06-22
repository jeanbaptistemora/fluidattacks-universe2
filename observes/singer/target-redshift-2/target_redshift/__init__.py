from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "0.1.0"

_conf = BugsnagConf(
    "target", __version__, "./observes/singer/target_redshift", False
)
set_bugsnag(_conf)
LOG = set_main_log(__name__)
