from lib_root.f406.cloudformation import (
    cfn_aws_efs_unencrypted,
)
from lib_root.f406.terraform import (
    tfm_aws_efs_unencrypted,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F406
QUERIES: graph_model.Queries = (
    (FINDING, cfn_aws_efs_unencrypted),
    (FINDING, tfm_aws_efs_unencrypted),
)
