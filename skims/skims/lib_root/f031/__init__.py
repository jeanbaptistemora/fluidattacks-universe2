from lib_root.f031.terraform import (
    tfm_admin_policy_attached,
    tfm_bucket_policy_allows_public_access,
    tfm_iam_excessive_privileges,
    tfm_iam_excessive_role_policy,
    tfm_iam_has_full_access_to_ssm,
    tfm_iam_user_missing_role_based_security,
    tfm_negative_statement,
    tfm_open_passrole,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F031
QUERIES: graph_model.Queries = (
    (FINDING, tfm_admin_policy_attached),
    (FINDING, tfm_bucket_policy_allows_public_access),
    (FINDING, tfm_iam_excessive_privileges),
    (FINDING, tfm_iam_excessive_role_policy),
    (FINDING, tfm_iam_has_full_access_to_ssm),
    (FINDING, tfm_iam_user_missing_role_based_security),
    (FINDING, tfm_negative_statement),
    (FINDING, tfm_open_passrole),
)
