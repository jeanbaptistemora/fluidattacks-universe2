# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f009.javascript import (
    js_crypto_js_credentials as javascript_crypto_js_credentials,
)
from lib_root.f009.typescript import (
    ts_crypto_js_credentials as typescript_crypto_ts_credentials,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F009
QUERIES: graph_model.Queries = (
    (FINDING, javascript_crypto_js_credentials),
    (FINDING, typescript_crypto_ts_credentials),
)
