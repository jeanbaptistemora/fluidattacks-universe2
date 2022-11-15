# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f353.javascript import (
    decode_insecure_jwt_token as js_decode_insecure_jwt_token,
)
from lib_root.f353.typescript import (
    decode_insecure_jwt_token as ts_decode_insecure_jwt_token,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F353
QUERIES: graph_model.Queries = (
    (FINDING, js_decode_insecure_jwt_token),
    (FINDING, ts_decode_insecure_jwt_token),
)
