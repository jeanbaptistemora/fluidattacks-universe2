from lib_root.f060.c_sharp import (
    insecure_exceptions as c_sharp_insecure_exceptions,
    throws_generic_exception as c_sharp_throws_generic_exception,
)
from lib_root.f060.java import (
    insecure_exceptions as java_insecure_exceptions,
    throws_generic_exception as java_throws_generic_exception,
)
from lib_root.f060.php import (
    insecure_exceptions as php_insecure_exceptions,
)
from lib_root.f060.ruby import (
    insecure_exceptions as ruby_insecure_exceptions,
)
from lib_root.f060.scala import (
    insecure_exceptions as scala_insecure_exceptions,
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
    (FINDING, php_insecure_exceptions),
    (FINDING, ruby_insecure_exceptions),
    (FINDING, scala_insecure_exceptions),
)
