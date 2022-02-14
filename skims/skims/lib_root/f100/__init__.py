from lib_root.f100.c_sharp import (
    insec_create as c_sharp_insec_create,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F100
QUERIES: graph_model.Queries = ((FINDING, c_sharp_insec_create),)
