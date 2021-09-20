from lib_root.f074.c_sharp import (
    commented_code as c_sharp_commented_code,
)
from lib_root.f074.java import (
    commented_code as java_commented_code,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F074
QUERIES: graph_model.Queries = (
    (FINDING, java_commented_code),
    (FINDING, c_sharp_commented_code),
)
