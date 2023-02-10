from lib_root.f408.terraform import (
    tfm_api_gateway_access_logging_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F408
QUERIES: graph_model.Queries = (
    (FINDING, tfm_api_gateway_access_logging_disabled),
)
