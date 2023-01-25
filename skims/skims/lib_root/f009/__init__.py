from lib_root.f009.conf_files import (
    sensitive_info_json as json_sensitive_info,
)
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
    (FINDING, json_sensitive_info),
    (FINDING, typescript_crypto_ts_credentials),
)
