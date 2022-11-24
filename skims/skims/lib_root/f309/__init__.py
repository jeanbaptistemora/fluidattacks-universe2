from lib_root.f309.javascript import (
    uses_insecure_jwt_token as js_uses_insecure_jwt_token,
)
from lib_root.f309.typescript import (
    ts_insecure_jwt_token,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F309
QUERIES: graph_model.Queries = (
    (FINDING, js_uses_insecure_jwt_token),
    (FINDING, ts_insecure_jwt_token),
)
