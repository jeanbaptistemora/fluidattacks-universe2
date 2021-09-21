from lib_root.f096.c_sharp import (
    insecure_deserialization as c_sharp_insecure_deserialization,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F096
QUERIES: graph_model.Queries = ((FINDING, c_sharp_insecure_deserialization),)
