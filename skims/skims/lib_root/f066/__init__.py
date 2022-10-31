# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f066.c_sharp import (
    has_console_functions as c_sharp_has_console_functions,
)
from lib_root.f066.javascript import (
    js_uses_console_log as javascript_uses_console_log,
)
from lib_root.f066.typescript import (
    ts_uses_console_log,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F066
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_has_console_functions),
    (FINDING, javascript_uses_console_log),
    (FINDING, ts_uses_console_log),
)
