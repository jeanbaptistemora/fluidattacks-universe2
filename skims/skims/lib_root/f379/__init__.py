from lib_root.f379.javascript import (
    js_import_is_never_used,
)
from lib_root.f379.typescript import (
    ts_import_is_never_used,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F379
QUERIES: graph_model.Queries = (
    (FINDING, ts_import_is_never_used),
    (FINDING, js_import_is_never_used),
)
