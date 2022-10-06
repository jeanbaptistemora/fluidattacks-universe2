# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f332.java import (
    csrf_protections_disabled as java_csrf_protections_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F332
QUERIES: graph_model.Queries = ((FINDING, java_csrf_protections_disabled),)
