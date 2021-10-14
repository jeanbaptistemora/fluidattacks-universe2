from lib_root.f060.c_sharp import (
    insecure_exceptions as c_sharp_insecure_exceptions,
    throws_generic_exception as c_sharp_throws_generic_exception,
)
from lib_root.f060.java import (
    insecure_exceptions as java_insecure_exceptions,
    throws_generic_exception as java_throws_generic_exception,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insecure_exceptions),
    (FINDING, c_sharp_throws_generic_exception),
    (FINDING, java_throws_generic_exception),
    (FINDING, java_insecure_exceptions),
)
