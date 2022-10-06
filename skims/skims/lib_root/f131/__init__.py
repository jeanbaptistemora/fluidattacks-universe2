# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f131.c_sharp import (
    check_default_usehsts as c_sharp_check_default_usehsts,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F131
QUERIES: graph_model.Queries = ((FINDING, c_sharp_check_default_usehsts),)
