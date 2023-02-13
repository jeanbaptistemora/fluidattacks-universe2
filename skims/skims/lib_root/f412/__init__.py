from lib_root.f412.terraform import (
    tfm_azure_key_vault_not_recoverable,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F412
QUERIES: graph_model.Queries = (
    (FINDING, tfm_azure_key_vault_not_recoverable),
)
