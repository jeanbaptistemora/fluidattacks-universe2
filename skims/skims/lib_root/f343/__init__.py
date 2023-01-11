from lib_root.f343.javascript import (
    js_insecure_compression as javascript_insecure_compression,
)
from lib_root.f343.typescript import (
    ts_insecure_compression as typescript_insecure_compression,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F343
QUERIES: graph_model.Queries = (
    (FINDING, javascript_insecure_compression),
    (FINDING, typescript_insecure_compression),
)
