from lib_root.f004.c_sharp import (
    remote_command_execution as c_sharp_remote_command_execution,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F004
QUERIES: graph_model.Queries = ((FINDING, c_sharp_remote_command_execution),)
