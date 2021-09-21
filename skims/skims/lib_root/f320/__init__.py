from lib_root.f320.c_sharp import (
    ldap_connections_authenticated as csharp_ldap_connections_authenticated,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F320
QUERIES: graph_model.Queries = (
    (FINDING, csharp_ldap_connections_authenticated),
)
