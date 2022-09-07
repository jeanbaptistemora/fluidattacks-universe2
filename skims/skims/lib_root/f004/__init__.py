# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f004.c_sharp import (
    remote_command_execution as c_sharp_remote_command_execution,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F004
QUERIES: graph_model.Queries = ((FINDING, c_sharp_remote_command_execution),)
