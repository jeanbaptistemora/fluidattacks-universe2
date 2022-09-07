# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from utils_logger.v2 import (
    BugsnagConf,
    set_bugsnag,
    set_main_log,
)

__version__ = "1.0.0"

_conf = BugsnagConf(
    "tap", __version__, "./observes/service/job_last_success", False
)
set_bugsnag(_conf)
LOG = set_main_log(__name__)
