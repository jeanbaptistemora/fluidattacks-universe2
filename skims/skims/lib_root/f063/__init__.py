from lib_root.f063.c_sharp import (
    open_redirect as c_sharp_open_redirect,
    unsafe_path_traversal as c_sharp_unsafe_path_traversal,
)
from lib_root.f063.java import (
    unsafe_path_traversal as java_unsafe_path_traversal,
    zip_slip_injection as java_zip_slip_injection,
)
from lib_root.f063.javascript import (
    javascript_insecure_path_traversal as js_insecure_path_traversal,
    zip_slip_injection as js_zip_slip_injection,
)
from lib_root.f063.python import (
    python_io_path_traversal,
)
from lib_root.f063.typescript import (
    ts_insecure_path_traversal,
    ts_zip_slip_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F063
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_open_redirect),
    (FINDING, c_sharp_unsafe_path_traversal),
    (FINDING, java_zip_slip_injection),
    (FINDING, java_unsafe_path_traversal),
    (FINDING, js_insecure_path_traversal),
    (FINDING, js_zip_slip_injection),
    (FINDING, python_io_path_traversal),
    (FINDING, ts_insecure_path_traversal),
    (FINDING, ts_zip_slip_injection),
)
