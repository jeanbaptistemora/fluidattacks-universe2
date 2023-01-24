from lib_root.f325.conf_files import (
    principal_wildcard as json_principal_wildcard,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F325
QUERIES: graph_model.Queries = ((FINDING, json_principal_wildcard),)
