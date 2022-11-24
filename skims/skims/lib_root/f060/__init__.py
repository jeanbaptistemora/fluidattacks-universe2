from lib_root.f060.c_sharp import (
    insecure_certificate_validation as csharp_insecure_certificate_validation,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
QUERIES: graph_model.Queries = (
    (FINDING, csharp_insecure_certificate_validation),
)
