from lib_root.f021.c_sharp import (
    xpath_injection as c_sharp_path_injection,
    xpath_injection_evaluate,
)
from lib_root.f021.javascript import (
    javascript_dynamic_xpath,
)
from lib_root.f021.typescript import (
    ts_dynamic_xpath,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F021
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_path_injection),
    (FINDING, xpath_injection_evaluate),
    (FINDING, javascript_dynamic_xpath),
    (FINDING, ts_dynamic_xpath),
)
