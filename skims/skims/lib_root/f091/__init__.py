from lib_root.f091.c_sharp import (
    insecure_logging as c_sharp_insecure_logging,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F091
QUERIES: graph_model.Queries = ((FINDING, c_sharp_insecure_logging),)
