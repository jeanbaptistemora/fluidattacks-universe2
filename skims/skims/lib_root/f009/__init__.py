from lib_root.f009.javascript import (
    crypto_js_credentials as javascript_crypto_js_credentials,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F009
QUERIES: graph_model.Queries = ((FINDING, javascript_crypto_js_credentials),)
