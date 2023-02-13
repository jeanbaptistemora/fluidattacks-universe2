from lib_root.f407.terraform import (
    tfm_aws_ebs_volumes_unencrypted,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F407
QUERIES: graph_model.Queries = ((FINDING, tfm_aws_ebs_volumes_unencrypted),)
