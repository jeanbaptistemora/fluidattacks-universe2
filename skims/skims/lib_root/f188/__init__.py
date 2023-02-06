from lib_root.f188.typescript import (
    lack_of_validation_dom_window,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F188
QUERIES: graph_model.Queries = ((FINDING, lack_of_validation_dom_window),)
