from lib_root.f059.java import (
    sensitive_log_info as java_sensitive_log_info,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F059
QUERIES: graph_model.Queries = ((FINDING, java_sensitive_log_info),)
