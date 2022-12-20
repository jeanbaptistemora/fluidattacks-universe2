from lib_root.f297.javascript import (
    sql_injection as js_sql_injection,
)
from lib_root.f297.typescript import (
    sql_injection as ts_sql_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F297
QUERIES: graph_model.Queries = (
    (FINDING, js_sql_injection),
    (FINDING, ts_sql_injection),
)
