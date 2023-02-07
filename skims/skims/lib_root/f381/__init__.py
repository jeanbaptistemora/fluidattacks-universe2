from lib_root.f381.terraform import (
    tfm_check_required_version,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F381
QUERIES: graph_model.Queries = ((FINDING, tfm_check_required_version),)
