from lib_root.f401.terraform import (
    tfm_azure_kv_secret_no_expiration_date,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F401
QUERIES: graph_model.Queries = (
    (FINDING, tfm_azure_kv_secret_no_expiration_date),
)
