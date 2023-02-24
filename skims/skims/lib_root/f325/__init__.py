from lib_root.f325.conf_files import (
    principal_wildcard as json_principal_wildcard,
)
from lib_root.f325.terraform import (
    tfm_iam_has_wildcard_resource_on_write_action,
    tfm_kms_key_has_master_keys_exposed_to_everyone,
    tfm_permissive_policy,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F325
QUERIES: graph_model.Queries = (
    (FINDING, json_principal_wildcard),
    (FINDING, tfm_iam_has_wildcard_resource_on_write_action),
    (FINDING, tfm_kms_key_has_master_keys_exposed_to_everyone),
    (FINDING, tfm_permissive_policy),
)
