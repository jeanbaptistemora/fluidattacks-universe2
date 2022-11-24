from lib_root.f413.c_sharp import (
    insecure_assembly_load as c_sharp_insecure_assembly_load,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F413
QUERIES: graph_model.Queries = ((FINDING, c_sharp_insecure_assembly_load),)
