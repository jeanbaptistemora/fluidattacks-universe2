from lib_root.f164.conf_files import (
    ssl_port_missing as json_ssl_port_missing,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F164
QUERIES: graph_model.Queries = ((FINDING, json_ssl_port_missing),)
