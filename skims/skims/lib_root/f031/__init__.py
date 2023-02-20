from lib_root.f031.terraform import (
    tfm_admin_policy_attached,
    tfm_iam_excessive_privileges,
    tfm_iam_user_missing_role_based_security,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F031
QUERIES: graph_model.Queries = (
    (FINDING, tfm_admin_policy_attached),
    (FINDING, tfm_iam_excessive_privileges),
    (FINDING, tfm_iam_user_missing_role_based_security),
)
