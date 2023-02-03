from lib_root.f246.terraform import (
    tfm_rds_has_unencrypted_storage,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F246
QUERIES: graph_model.Queries = ((FINDING, tfm_rds_has_unencrypted_storage),)
