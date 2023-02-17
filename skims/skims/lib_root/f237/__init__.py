from lib_root.f237.dart import (
    has_print_statements as dart_has_print_statements,
)
from lib_root.f237.java import (
    has_print_statements as java_has_print_statements,
)
from lib_root.f237.python import (
    has_print_statements as python_has_print_statements,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F237
QUERIES: graph_model.Queries = (
    (FINDING, dart_has_print_statements),
    (FINDING, java_has_print_statements),
    (FINDING, python_has_print_statements),
)
