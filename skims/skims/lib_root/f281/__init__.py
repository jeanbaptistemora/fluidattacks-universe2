from lib_root.f281.terraform import (
    tfm_bucket_policy_has_secure_transport,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F281
QUERIES: graph_model.Queries = (
    (FINDING, tfm_bucket_policy_has_secure_transport),
)
