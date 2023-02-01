from lib_root.f109.terraform import (
    tfm_rds_instance_inside_subnet,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F109
QUERIES: graph_model.Queries = ((FINDING, tfm_rds_instance_inside_subnet),)
