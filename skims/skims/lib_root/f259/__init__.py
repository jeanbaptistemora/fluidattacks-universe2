from lib_root.f259.terraform import (
    tfm_db_no_point_in_time_recovery,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F259
QUERIES: graph_model.Queries = ((FINDING, tfm_db_no_point_in_time_recovery),)
