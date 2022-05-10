from lib_root.f098.c_sharp import (
    path_injection as c_sharp_path_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F098
QUERIES: graph_model.Queries = ((FINDING, c_sharp_path_injection),)
