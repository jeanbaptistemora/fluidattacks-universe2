from lib_root.f099.terraform import (
    tfm_unencrypted_buckets,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F099
QUERIES: graph_model.Queries = ((FINDING, tfm_unencrypted_buckets),)
