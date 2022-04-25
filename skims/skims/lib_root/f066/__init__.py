from lib_root.f066.c_sharp import (
    has_console_functions as c_sharp_has_console_functions,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F066
QUERIES: graph_model.Queries = ((FINDING, c_sharp_has_console_functions),)
