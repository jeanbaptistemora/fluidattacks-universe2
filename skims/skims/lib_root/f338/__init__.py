from lib_root.f338.c_sharp import (
    check_hashes_salt as csharp_check_hashes_salt,
)
from lib_root.f338.java import (
    java_salting_is_harcoded,
)
from lib_root.f338.javascript import (
    js_salting_is_harcoded,
)
from lib_root.f338.typescript import (
    ts_salting_is_harcoded,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F338
QUERIES: graph_model.Queries = (
    (FINDING, csharp_check_hashes_salt),
    (FINDING, js_salting_is_harcoded),
    (FINDING, ts_salting_is_harcoded),
    (FINDING, java_salting_is_harcoded),
)
