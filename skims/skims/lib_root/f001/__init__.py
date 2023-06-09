from lib_root.f001.c_sharp import (
    sql_injection as c_sharp_sql_injection,
    sql_user_params as c_sharp_sql_user_params,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F001
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_sql_injection),
    (FINDING, c_sharp_sql_user_params),
)
