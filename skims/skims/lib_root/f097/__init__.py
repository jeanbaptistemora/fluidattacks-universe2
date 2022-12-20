from lib_root.f097.javascript import (
    has_reverse_tabnabbing as js_has_reverse_tabnabbing,
)
from lib_root.f097.typescript import (
    has_reverse_tabnabbing as ts_has_reverse_tabnabbing,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F097
QUERIES: graph_model.Queries = (
    (FINDING, js_has_reverse_tabnabbing),
    (FINDING, ts_has_reverse_tabnabbing),
)
