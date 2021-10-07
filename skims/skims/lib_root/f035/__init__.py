from lib_root.f035.c_sharp import (
    no_password as csharp_no_password,
    weak_credential_policy as csharp_weak_credential_policy,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F035
QUERIES: graph_model.Queries = (
    (FINDING, csharp_weak_credential_policy),
    (FINDING, csharp_no_password),
)
