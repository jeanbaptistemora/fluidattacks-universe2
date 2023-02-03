from lib_root.f256.terraform import (
    tfm_db_has_not_automated_backups,
    tfm_rds_has_not_automated_backups,
    tfm_rds_no_deletion_protection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F256
QUERIES: graph_model.Queries = (
    (FINDING, tfm_db_has_not_automated_backups),
    (FINDING, tfm_rds_has_not_automated_backups),
    (FINDING, tfm_rds_no_deletion_protection),
)
