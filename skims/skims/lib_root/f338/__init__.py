from lib_root.f338.c_sharp import (
    check_hashes_salt as csharp_check_hashes_salt,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F338
QUERIES: graph_model.Queries = ((FINDING, csharp_check_hashes_salt),)
