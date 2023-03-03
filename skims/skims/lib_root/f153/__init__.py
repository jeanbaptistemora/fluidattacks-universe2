from lib_root.f153.java import (
    java_accepts_any_mime_type_chain,
    java_http_accepts_any_mime_type,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F153
QUERIES: graph_model.Queries = (
    (FINDING, java_accepts_any_mime_type_chain),
    (FINDING, java_http_accepts_any_mime_type),
)
