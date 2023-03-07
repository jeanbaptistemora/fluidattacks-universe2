from lib_root.f428.conf_files import (
    json_invalid_file,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F428
QUERIES: graph_model.Queries = ((FINDING, json_invalid_file),)
