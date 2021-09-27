from lib_root.f034.javascript import (
    weak_random as javscript_weak_random,
)
from model import (
    core_model,
)
from model.graph_model import (
    Queries,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: Queries = ((FINDING, javscript_weak_random),)
