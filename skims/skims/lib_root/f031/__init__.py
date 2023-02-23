from lib_root.f031.terraform import (
    terraform_negative_statement,
    terraform_open_passrole,
    tfm_admin_policy_attached,
    tfm_bucket_policy_allows_public_access,
    tfm_iam_excessive_privileges,
    tfm_iam_has_full_access_to_ssm,
    tfm_iam_user_missing_role_based_security,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F031
QUERIES: graph_model.Queries = (
    (FINDING, terraform_negative_statement),
    (FINDING, terraform_open_passrole),
    (FINDING, tfm_admin_policy_attached),
    (FINDING, tfm_bucket_policy_allows_public_access),
    (FINDING, tfm_iam_excessive_privileges),
    (FINDING, tfm_iam_has_full_access_to_ssm),
    (FINDING, tfm_iam_user_missing_role_based_security),
)
