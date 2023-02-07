from lib_root.f372.conf_files import (
    https_flag_missing as json_https_flag_missing,
)
from lib_root.f372.terraform import (
    tfm_azure_kv_only_accessible_over_https,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F372
QUERIES: graph_model.Queries = (
    (FINDING, json_https_flag_missing),
    (FINDING, tfm_azure_kv_only_accessible_over_https),
)
