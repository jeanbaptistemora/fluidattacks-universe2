from lib_root.f042.c_sharp import (
    insecurely_generated_cookies as csharp_insecurely_generated_cookies,
)
from lib_root.f042.java import (
    java_insecure_cookie,
)
from lib_root.f042.javascript import (
    insecurely_generated_cookies as js_insecurely_generated_cookies,
)
from lib_root.f042.typescript import (
    insecurely_generated_cookies as ts_insecurely_generated_cookies,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F042
QUERIES: graph_model.Queries = (
    (FINDING, csharp_insecurely_generated_cookies),
    (FINDING, java_insecure_cookie),
    (FINDING, js_insecurely_generated_cookies),
    (FINDING, ts_insecurely_generated_cookies),
)
