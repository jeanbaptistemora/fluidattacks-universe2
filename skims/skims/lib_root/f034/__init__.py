# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f034.javascript import (
    weak_random as javscript_weak_random,
)
from model import (
    core_model,
)
from model.graph_model import (
    Queries,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F034
QUERIES: Queries = ((FINDING, javscript_weak_random),)
