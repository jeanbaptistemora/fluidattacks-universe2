from lib_root.f416.c_sharp import (
    xaml_injection as c_sharp_xaml_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F416
QUERIES: graph_model.Queries = ((FINDING, c_sharp_xaml_injection),)
