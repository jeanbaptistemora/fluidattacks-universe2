from lib_root.f070.go import (
    wildcard_import as java_wildcard_import,
)
from lib_root.f070.java import (
    wildcard_import as go_wildcard_import,
)
from lib_root.f070.kotlin import (
    wildcard_import as kotlin_wildcard_import,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F070
QUERIES: graph_model.Queries = (
    (FINDING, java_wildcard_import),
    (FINDING, go_wildcard_import),
    (FINDING, kotlin_wildcard_import),
)
