from lib_root.f157.terraform import (
    tfm_aws_acl_broad_network_access,
    tfm_azure_kv_danger_bypass,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F157
QUERIES: graph_model.Queries = (
    (FINDING, tfm_aws_acl_broad_network_access),
    (FINDING, tfm_azure_kv_danger_bypass),
)
