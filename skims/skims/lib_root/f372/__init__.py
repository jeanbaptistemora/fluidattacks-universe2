from lib_root.f372.json import (
    https_flag_missing as json_https_flag_missing,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F372
QUERIES: graph_model.Queries = ((FINDING, json_https_flag_missing),)
