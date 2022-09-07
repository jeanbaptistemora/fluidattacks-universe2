# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f012.java import (
    jpa_like as java_jpa_like,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F012
QUERIES: graph_model.Queries = ((FINDING, java_jpa_like),)
