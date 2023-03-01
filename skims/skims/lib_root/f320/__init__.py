from lib_root.f320.c_sharp import (
    cs_ldap_connections_authenticated,
)
from lib_root.f320.python import (
    python_unsafe_ldap_connection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F320
QUERIES: graph_model.Queries = (
    (FINDING, cs_ldap_connections_authenticated),
    (FINDING, python_unsafe_ldap_connection),
)
