from lib_root.f259.cloudformation import (
    cfn_has_not_point_in_time_recovery,
)
from lib_root.f259.terraform import (
    tfm_db_no_point_in_time_recovery,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F259
QUERIES: graph_model.Queries = (
    (FINDING, cfn_has_not_point_in_time_recovery),
    (FINDING, tfm_db_no_point_in_time_recovery),
)
