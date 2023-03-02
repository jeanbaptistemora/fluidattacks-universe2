from lib_root.f211.c_sharp import (
    regex_injection as csharp_regex_injection,
    vuln_regular_expression as csharp_vuln_regular_expression,
)
from lib_root.f211.java import (
    java_vuln_regular_expression,
)
from lib_root.f211.javascript import (
    regex_injection as js_regex_injection,
)
from lib_root.f211.python import (
    python_regex_dos,
)
from lib_root.f211.typescript import (
    regex_injection as ts_regex_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F211
QUERIES: graph_model.Queries = (
    (FINDING, csharp_vuln_regular_expression),
    (FINDING, csharp_regex_injection),
    (FINDING, java_vuln_regular_expression),
    (FINDING, js_regex_injection),
    (FINDING, python_regex_dos),
    (FINDING, ts_regex_injection),
)
