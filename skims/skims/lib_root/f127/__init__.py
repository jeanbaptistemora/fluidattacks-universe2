from lib_root.f127.go import (
    go_insecure_query_float,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F127
QUERIES: graph_model.Queries = ((FINDING, go_insecure_query_float),)
