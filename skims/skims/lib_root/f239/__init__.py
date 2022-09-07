# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f239.c_sharp import (
    info_leak_errors as c_sharp_info_leak_errors,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F239
QUERIES: graph_model.Queries = ((FINDING, c_sharp_info_leak_errors),)
