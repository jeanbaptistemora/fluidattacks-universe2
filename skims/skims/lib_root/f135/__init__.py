# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f135.javascript import (
    javascript_insecure_http_headers,
)
from lib_root.f135.typescript import (
    typescript_insecure_http_headers,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F135
QUERIES: graph_model.Queries = (
    (FINDING, typescript_insecure_http_headers),
    (FINDING, javascript_insecure_http_headers),
)
