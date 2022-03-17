from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
    start_session,
)

__version__ = "1.0.0"
set_bugsnag(BugsnagConf("service", __version__, __file__, False))
start_session()
LOG = set_main_log(__name__)
