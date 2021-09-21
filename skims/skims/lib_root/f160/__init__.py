from lib_root.f160.c_sharp import (
    file_create_temp_file as csharp_file_create_temp_file,
)
from lib_root.f160.java import (
    file_create_temp_file as java_file_create_temp_file,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F160
QUERIES: graph_model.Queries = (
    (FINDING, java_file_create_temp_file),
    (FINDING, csharp_file_create_temp_file),
)
