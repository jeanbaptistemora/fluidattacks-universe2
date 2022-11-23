# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f280.typescript import (
    non_secure_construction_of_cookies as ts_non_secure_construction,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F280
QUERIES: graph_model.Queries = ((FINDING, ts_non_secure_construction),)
