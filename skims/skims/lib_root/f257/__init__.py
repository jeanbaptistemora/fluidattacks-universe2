from lib_root.f257.cloudformation import (
    cfn_ec2_has_not_termination_protection,
)
from lib_root.f257.terraform import (
    tfm_ec2_has_not_termination_protection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F257
QUERIES: graph_model.Queries = (
    (FINDING, cfn_ec2_has_not_termination_protection),
    (FINDING, tfm_ec2_has_not_termination_protection),
)
