from lib_root.f239.c_sharp import (
    info_leak_errors as c_sharp_info_leak_errors,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F239
QUERIES: graph_model.Queries = ((FINDING, c_sharp_info_leak_errors),)
