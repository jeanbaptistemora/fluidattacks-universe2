from lib_root.f004.c_sharp import (
    remote_command_execution as c_sharp_remote_command_execution,
)
from lib_root.f004.java import (
    remote_command_execution as java_remote_command_execution,
)
from lib_root.f004.javascript import (
    remote_command_execution as js_remote_command_execution,
)
from lib_root.f004.typescript import (
    remote_command_execution as ts_remote_command_execution,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F004
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_remote_command_execution),
    (FINDING, java_remote_command_execution),
    (FINDING, js_remote_command_execution),
    (FINDING, ts_remote_command_execution),
)
