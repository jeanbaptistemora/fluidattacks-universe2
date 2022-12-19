from lib_root.f063.c_sharp import (
    open_redirect as c_sharp_open_redirect,
)
from lib_root.f063.java import (
    zip_slip_injection as java_zip_slip_injection,
)
from lib_root.f063.javascript import (
    javascript_insecure_path_traversal as js_insecure_path_traversal,
    zip_slip_injection as js_zip_slip_injection,
)
from lib_root.f063.typescript import (
    typescript_insecure_path_traversal,
    zip_slip_injection as ts_zip_slip_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F063
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_open_redirect),
    (FINDING, java_zip_slip_injection),
    (FINDING, js_insecure_path_traversal),
    (FINDING, js_zip_slip_injection),
    (FINDING, ts_zip_slip_injection),
    (FINDING, typescript_insecure_path_traversal),
)
