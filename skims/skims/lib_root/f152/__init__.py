# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f152.typescript import (
    insecure_header_xframe_options as typescript_insecure_header_xframe_opts,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F152
QUERIES: graph_model.Queries = (
    (FINDING, typescript_insecure_header_xframe_opts),
)
