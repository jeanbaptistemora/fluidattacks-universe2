from lib_root.f153.java import (
    java_http_accepts_any_myme_type,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F153
QUERIES: graph_model.Queries = ((FINDING, java_http_accepts_any_myme_type),)
