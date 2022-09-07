# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f001.c_sharp import (
    sql_injection as c_sharp_sql_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F001
QUERIES: graph_model.Queries = ((FINDING, c_sharp_sql_injection),)
