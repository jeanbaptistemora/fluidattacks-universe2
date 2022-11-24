from lib_root.f007.java import (
    csrf_protections_disabled as java_csrf_protections_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F007
QUERIES: graph_model.Queries = ((FINDING, java_csrf_protections_disabled),)
