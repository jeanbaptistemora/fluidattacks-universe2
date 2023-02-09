from lib_root.f414.c_sharp import (
    disabled_http_header_check as c_sharp_disabled_http_header_check,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F414
QUERIES: graph_model.Queries = ((FINDING, c_sharp_disabled_http_header_check),)
