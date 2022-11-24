from lib_root.f012.java import (
    jpa_like as java_jpa_like,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F012
QUERIES: graph_model.Queries = ((FINDING, java_jpa_like),)
