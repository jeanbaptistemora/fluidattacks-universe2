from lib_root.f258.terraform import (
    tfm_elb2_has_not_deletion_protection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F258
QUERIES: graph_model.Queries = (
    (FINDING, tfm_elb2_has_not_deletion_protection),
)
