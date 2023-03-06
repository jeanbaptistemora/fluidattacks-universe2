from lib_root.f250.cloudformation import (
    cfn_ec2_has_unencrypted_volumes,
    cfn_ec2_instance_unencrypted_ebs_block_devices,
)
from lib_root.f250.terraform import (
    tfm_ebs_unencrypted_by_default,
    tfm_ebs_unencrypted_volumes,
    tfm_ec2_instance_unencrypted_ebs_block_devices,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F250
QUERIES: graph_model.Queries = (
    (FINDING, cfn_ec2_has_unencrypted_volumes),
    (FINDING, cfn_ec2_instance_unencrypted_ebs_block_devices),
    (FINDING, tfm_ebs_unencrypted_by_default),
    (FINDING, tfm_ebs_unencrypted_volumes),
    (FINDING, tfm_ec2_instance_unencrypted_ebs_block_devices),
)
