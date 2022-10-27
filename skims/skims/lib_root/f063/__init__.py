# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f063.c_sharp import (
    open_redirect as c_sharp_open_redirect,
)
from lib_root.f063.javascript import (
    insecure_path_traversal as js_insecure_path_traversal,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F063
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_open_redirect),
    (FINDING, js_insecure_path_traversal),
)
