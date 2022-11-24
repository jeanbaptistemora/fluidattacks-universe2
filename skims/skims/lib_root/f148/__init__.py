from lib_root.f148.c_sharp import (
    cs_insecure_channel,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F148
QUERIES: graph_model.Queries = ((FINDING, cs_insecure_channel),)
