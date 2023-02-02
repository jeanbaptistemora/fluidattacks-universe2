from lib_root.f203.terraform import (
    tfm_public_buckets,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F203
QUERIES: graph_model.Queries = ((FINDING, tfm_public_buckets),)
