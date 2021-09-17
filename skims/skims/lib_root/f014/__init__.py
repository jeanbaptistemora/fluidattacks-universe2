from lib_root.f014.go import (
    float_currency as go_float_currency,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F109
QUERIES: graph_model.Queries = ((FINDING, go_float_currency),)
