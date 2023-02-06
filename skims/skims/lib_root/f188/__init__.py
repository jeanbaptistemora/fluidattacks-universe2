from lib_root.f188.javascript import (
    jsx_lack_of_validation_dom_window,
)
from lib_root.f188.typescript import (
    tsx_lack_of_validation_dom_window,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F188
QUERIES: graph_model.Queries = (
    (FINDING, tsx_lack_of_validation_dom_window),
    (FINDING, jsx_lack_of_validation_dom_window),
)
