from lib_root.f300.terraform import (
    tfm_azure_app_authentication_off,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F300
QUERIES: graph_model.Queries = ((FINDING, tfm_azure_app_authentication_off),)
