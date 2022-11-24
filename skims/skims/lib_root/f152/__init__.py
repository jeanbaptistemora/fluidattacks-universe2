from lib_root.f152.javascript import (
    javascript_insecure_header_xframe_options,
)
from lib_root.f152.typescript import (
    typescript_insecure_header_xframe_options,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F152
QUERIES: graph_model.Queries = (
    (FINDING, typescript_insecure_header_xframe_options),
    (FINDING, javascript_insecure_header_xframe_options),
)
