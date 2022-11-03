# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f371.javascript import (
    js_bypass_security_trust_url,
    js_dangerously_set_innerhtml,
    uses_innerhtml as js_uses_innerhtml,
)
from lib_root.f371.typescript import (
    ts_bypass_security_trust_url,
    ts_dangerously_set_innerhtml,
    uses_innerhtml as ts_uses_innerhtml,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F371
QUERIES: graph_model.Queries = (
    (FINDING, js_uses_innerhtml),
    (FINDING, ts_uses_innerhtml),
    (FINDING, js_bypass_security_trust_url),
    (FINDING, ts_bypass_security_trust_url),
    (FINDING, js_dangerously_set_innerhtml),
    (FINDING, ts_dangerously_set_innerhtml),
)
