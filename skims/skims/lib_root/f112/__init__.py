from lib_root.f112.java import (
    sql_injection as java_sql_injection,
)
from lib_root.f112.javascript import (
    unsafe_sql_injection as javascript_sql_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F112
QUERIES: graph_model.Queries = (
    (FINDING, java_sql_injection),
    (FINDING, javascript_sql_injection),
)
