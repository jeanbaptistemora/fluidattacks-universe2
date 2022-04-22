from lib_root.f016.c_sharp import (
    weak_protocol as c_sharp_weak_protocol,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F016
QUERIES: graph_model.Queries = ((FINDING, c_sharp_weak_protocol),)
