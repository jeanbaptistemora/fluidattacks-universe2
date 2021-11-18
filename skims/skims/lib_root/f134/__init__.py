from lib_root.f134.c_sharp import (
    insecure_cors as csharp_insecure_cors,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F134
QUERIES: graph_model.Queries = ((FINDING, csharp_insecure_cors),)
