# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f015.java import (
    insecure_authentication as java_insecure_authentication,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F015
QUERIES: graph_model.Queries = ((FINDING, java_insecure_authentication),)