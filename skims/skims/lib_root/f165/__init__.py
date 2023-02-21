from lib_root.f165.terraform import (
    tfm_iam_role_is_over_privileged,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F165
QUERIES: graph_model.Queries = ((FINDING, tfm_iam_role_is_over_privileged),)
