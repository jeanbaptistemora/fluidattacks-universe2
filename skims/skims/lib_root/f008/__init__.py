from lib_root.f008.typescript import (
    reflected_xss as ts_reflected_xss,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F008
QUERIES: graph_model.Queries = ((FINDING, ts_reflected_xss),)
