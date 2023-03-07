from lib_root.f394.cloudformation import (
    cfn_log_files_not_validated,
)
from lib_root.f394.terraform import (
    tfm_trail_log_files_not_validated,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F394
QUERIES: graph_model.Queries = (
    (FINDING, cfn_log_files_not_validated),
    (FINDING, tfm_trail_log_files_not_validated),
)
