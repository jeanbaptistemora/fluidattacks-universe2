from lib_root.f257.terraform import (
    ec2_has_not_termination_protection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F257
QUERIES: graph_model.Queries = ((FINDING, ec2_has_not_termination_protection),)
