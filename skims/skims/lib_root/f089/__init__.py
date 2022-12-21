from lib_root.f089.java import (
    trust_boundary_violation as java_trust_boundary_violation,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F089
QUERIES: graph_model.Queries = ((FINDING, java_trust_boundary_violation),)
