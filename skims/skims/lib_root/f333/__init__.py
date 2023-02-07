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
    (FINDING, tfm_ec2_associate_public_ip_address),
    (FINDING, tfm_ec2_has_not_an_iam_instance_profile),
    (FINDING, tfm_ec2_has_terminate_shutdown_behavior),
)
