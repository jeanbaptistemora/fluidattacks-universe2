from lib_root.f177.cloudformation import (
    cfn_ec2_use_default_security_group,
)
from lib_root.f177.terraform import (
    ec2_use_default_security_group,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F177
QUERIES: graph_model.Queries = (
    (FINDING, cfn_ec2_use_default_security_group),
    (FINDING, ec2_use_default_security_group),
)
