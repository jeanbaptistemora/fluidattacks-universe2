from lib_root.f034.java import (
    java_weak_random,
)
from lib_root.f034.javascript import (
    js_weak_random as javascript_weak_random,
)
from lib_root.f034.kotlin import (
    kt_weak_random as kotlin_weak_random,
)
from lib_root.f034.typescript import (
    ts_weak_random as typescript_weak_random,
)
from model import (
    core_model,
)
from model.graph_model import (
    Queries,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F034
QUERIES: Queries = (
    (FINDING, java_weak_random),
    (FINDING, javascript_weak_random),
    (FINDING, kotlin_weak_random),
    (FINDING, typescript_weak_random),
)
