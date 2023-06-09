from lib_root.f128.javascript import (
    javascript_insecure_cookies,
)
from lib_root.f128.typescript import (
    typescript_insecure_cookies,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F128
QUERIES: graph_model.Queries = (
    (FINDING, javascript_insecure_cookies),
    (FINDING, typescript_insecure_cookies),
)
