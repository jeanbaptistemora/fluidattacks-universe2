# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f350.java import (
    use_insecure_trust_manager as java_use_insecure_trust_manager,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F350
QUERIES: graph_model.Queries = ((FINDING, java_use_insecure_trust_manager),)
