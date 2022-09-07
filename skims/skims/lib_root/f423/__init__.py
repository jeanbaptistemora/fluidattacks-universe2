# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f423.java import (
    uses_exit_method as java_uses_exit_method,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F423
QUERIES: graph_model.Queries = ((FINDING, java_uses_exit_method),)
