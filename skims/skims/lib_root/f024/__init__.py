from lib_root.f024.terraform import (
    tfm_ec2_instances_without_profile,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F024
QUERIES: graph_model.Queries = ((FINDING, tfm_ec2_instances_without_profile),)
