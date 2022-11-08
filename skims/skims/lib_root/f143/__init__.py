# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f143.javascript import (
    uses_eval as js_uses_eval,
)
from lib_root.f143.typescript import (
    uses_eval as ts_uses_eval,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F143
QUERIES: graph_model.Queries = (
    (FINDING, js_uses_eval),
    (FINDING, ts_uses_eval),
)
