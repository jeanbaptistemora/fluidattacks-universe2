from lib_root.f424.java import (
    uses_exit_method as java_uses_exit_method,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F234
QUERIES: graph_model.Queries = ((FINDING, java_uses_exit_method),)
