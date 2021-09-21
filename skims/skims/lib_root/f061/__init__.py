from lib_root.f061.c_sharp import (
    swallows_exceptions as c_sharp_swallows_exceptions,
)
from lib_root.f061.java import (
    swallows_exceptions as java_swallows_exceptions,
)
from lib_root.f061.javascript import (
    swallows_exceptions as javascript_swallows_exceptions,
)
from lib_root.f061.kotlin import (
    swallows_exceptions as kotlin_swallows_exceptions,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F061
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_swallows_exceptions),
    (FINDING, java_swallows_exceptions),
    (FINDING, javascript_swallows_exceptions),
    (FINDING, kotlin_swallows_exceptions),
)
