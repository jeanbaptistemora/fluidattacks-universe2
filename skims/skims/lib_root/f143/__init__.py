from lib_root.f143.javascript import (
    uses_eval,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F143
QUERIES: graph_model.Queries = ((FINDING, uses_eval),)
