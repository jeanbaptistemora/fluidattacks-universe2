# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f371.javascript import (
    uses_innerhtml as js_uses_innerhtml,
)
from lib_root.f371.typescript import (
    uses_innerhtml as ts_uses_innerhtml,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F371
QUERIES: graph_model.Queries = (
    (FINDING, js_uses_innerhtml),
    (FINDING, ts_uses_innerhtml),
)
