from lib_root.f056.conf_files import (
    anon_connection_config as json_anon_connection_config,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F056
QUERIES: graph_model.Queries = ((FINDING, json_anon_connection_config),)
