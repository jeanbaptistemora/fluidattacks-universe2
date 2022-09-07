# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f022.kotlin import (
    unencrypted_channel as kotlin_unencrypted_channel,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F022
QUERIES: graph_model.Queries = ((FINDING, kotlin_unencrypted_channel),)
