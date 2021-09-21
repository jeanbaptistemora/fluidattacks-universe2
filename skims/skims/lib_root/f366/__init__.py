from lib_root.f366.c_sharp import (
    conflicting_annotations as csharp_conflicting_annotations,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F366
QUERIES: graph_model.Queries = ((FINDING, csharp_conflicting_annotations),)
