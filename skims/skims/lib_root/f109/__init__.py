from lib_root.f109.cloudformation import (
    cfn_rds_is_not_inside_a_db_subnet_group,
)
from lib_root.f109.terraform import (
    tfm_db_cluster_inside_subnet,
    tfm_rds_instance_inside_subnet,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F109
QUERIES: graph_model.Queries = (
    (FINDING, cfn_rds_is_not_inside_a_db_subnet_group),
    (FINDING, tfm_db_cluster_inside_subnet),
    (FINDING, tfm_rds_instance_inside_subnet),
)
