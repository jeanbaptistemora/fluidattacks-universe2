from lib_root.f085.javascript import (
    javascript_client_storage,
)
from lib_root.f085.typescript import (
    typescript_client_storage,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F085
QUERIES: graph_model.Queries = (
    (FINDING, javascript_client_storage),
    (FINDING, typescript_client_storage),
)
