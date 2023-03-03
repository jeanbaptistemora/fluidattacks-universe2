from lib_root.f246.cloudformation import (
    cfn_rds_has_unencrypted_storage,
)
from lib_root.f246.terraform import (
    tfm_db_has_unencrypted_storage,
    tfm_rds_has_unencrypted_storage,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F246
QUERIES: graph_model.Queries = (
    (FINDING, cfn_rds_has_unencrypted_storage),
    (FINDING, tfm_db_has_unencrypted_storage),
    (FINDING, tfm_rds_has_unencrypted_storage),
)
