from lib_root.f192.javascript import (
    reflected_xss as js_reflected_xss,
)
from lib_root.f192.typescript import (
    reflected_xss as ts_reflected_xss,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F192
QUERIES: graph_model.Queries = (
    (FINDING, js_reflected_xss),
    (FINDING, ts_reflected_xss),
)
