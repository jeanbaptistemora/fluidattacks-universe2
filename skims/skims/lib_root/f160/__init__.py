from lib_root.f160.c_sharp import (
    c_sharp_file_create_temp_file,
)
from lib_root.f160.java import (
    java_file_create_temp_file,
)
from lib_root.f160.python import (
    python_unsafe_temp_file,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F160
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_file_create_temp_file),
    (FINDING, java_file_create_temp_file),
    (FINDING, python_unsafe_temp_file),
)
