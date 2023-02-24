from lib_root.f358.c_sharp import (
    cert_validation_disabled as csharp_cert_validation_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F358
QUERIES: graph_model.Queries = ((FINDING, csharp_cert_validation_disabled),)
