from lib_root.f280.javascript import (
    non_secure_construction_of_cookies as js_non_secure_construction,
)
from lib_root.f280.python import (
    python_xml_parser,
)
from lib_root.f280.typescript import (
    non_secure_construction_of_cookies as ts_non_secure_construction,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F280
QUERIES: graph_model.Queries = (
    (FINDING, js_non_secure_construction),
    (FINDING, python_xml_parser),
    (FINDING, ts_non_secure_construction),
)
