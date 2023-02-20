from lib_root.f083.javascript import (
    js_xml_parser,
)
from lib_root.f083.python import (
    python_xml_parser,
)
from lib_root.f083.typescript import (
    ts_xml_parser,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F083
QUERIES: graph_model.Queries = (
    (FINDING, js_xml_parser),
    (FINDING, python_xml_parser),
    (FINDING, ts_xml_parser),
)
