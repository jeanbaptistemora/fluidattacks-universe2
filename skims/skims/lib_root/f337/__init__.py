from lib_root.f337.c_sharp import (
    has_not_csfr_protection as csharp_has_not_csfr_protection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F337
QUERIES: graph_model.Queries = ((FINDING, csharp_has_not_csfr_protection),)
