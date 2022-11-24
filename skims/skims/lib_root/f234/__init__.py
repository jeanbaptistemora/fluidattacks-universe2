from lib_root.f234.java import (
    info_leak_stacktrace as java_info_leak_stacktrace,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F234
QUERIES: graph_model.Queries = ((FINDING, java_info_leak_stacktrace),)
