# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class SupportedStreams(Enum):
    ALERT_CHS = "ALERT_CHS"
    CHECKS = "CHECKS"
    CHECK_GROUPS = "CHECK_GROUPS"
    CHECK_RESULTS = "CHECK_RESULTS"
    CHECK_STATUS = "CHECK_STATUS"
    DASHBOARD = "DASHBOARD"
    ENV_VARS = "ENV_VARS"
    MAINTENACE_WINDOWS = "MAINTENACE_WINDOWS"
    REPORTS = "REPORTS"
    SNIPPETS = "SNIPPETS"
