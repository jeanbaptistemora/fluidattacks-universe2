# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f368.java import (
    host_key_checking as java_host_key_checking,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F368
QUERIES: graph_model.Queries = ((FINDING, java_host_key_checking),)
