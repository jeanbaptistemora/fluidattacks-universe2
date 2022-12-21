from lib_root.f107.c_sharp import (
    ldap_injection as c_sharp_ldap_injection,
)
from lib_root.f107.java import (
    ldap_injection as java_ldap_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F107
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_ldap_injection),
    (FINDING, java_ldap_injection),
)
