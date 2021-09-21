from lib_root.f211.c_sharp import (
    vuln_regular_expression as csharp_vuln_regular_expression,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F211
QUERIES: graph_model.Queries = ((FINDING, csharp_vuln_regular_expression),)
