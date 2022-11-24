from lib_root.f021.c_sharp import (
    xpath_injection as c_sharp_path_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F021
QUERIES: graph_model.Queries = ((FINDING, c_sharp_path_injection),)
