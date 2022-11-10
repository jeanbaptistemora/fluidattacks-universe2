# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f034.javascript import (
    js_weak_random as javascript_weak_random,
)
from lib_root.f034.typescript import (
    ts_weak_random as typescript_weak_random,
)
from model import (
    core_model,
)
from model.graph_model import (
    Queries,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F034
QUERIES: Queries = (
    (FINDING, javascript_weak_random),
    (FINDING, typescript_weak_random),
)
