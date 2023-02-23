from lib_root.f091.c_sharp import (
    insecure_logging as c_sharp_insecure_logging,
)
from lib_root.f091.dart import (
    dart_insecure_logging,
)
from lib_root.f091.java import (
    insecure_logging as java_insecure_logging,
)
from lib_root.f091.javascript import (
    javascript_insecure_logging,
)
from lib_root.f091.typescript import (
    typescript_insecure_logging,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F091
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insecure_logging),
    (FINDING, java_insecure_logging),
    (FINDING, javascript_insecure_logging),
    (FINDING, typescript_insecure_logging),
    (FINDING, dart_insecure_logging),
)
