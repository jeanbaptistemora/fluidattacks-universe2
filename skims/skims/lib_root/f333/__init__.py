from lib_root.f333.cloudformation import (
    cfn_ec2_associate_public_ip_address,
    cfn_ec2_has_not_an_iam_instance_profile,
    cfn_ec2_has_terminate_shutdown_behavior,
)
from lib_root.f333.terraform import (
    tfm_ec2_associate_public_ip_address,
    tfm_ec2_has_not_an_iam_instance_profile,
    tfm_ec2_has_terminate_shutdown_behavior,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F333
QUERIES: graph_model.Queries = (
    (FINDING, cfn_ec2_associate_public_ip_address),
    (FINDING, cfn_ec2_has_terminate_shutdown_behavior),
    (FINDING, cfn_ec2_has_not_an_iam_instance_profile),
    (FINDING, tfm_ec2_associate_public_ip_address),
    (FINDING, tfm_ec2_has_not_an_iam_instance_profile),
    (FINDING, tfm_ec2_has_terminate_shutdown_behavior),
)
