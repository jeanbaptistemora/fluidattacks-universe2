from lib_root.f236.conf_files import (
    tsconfig_sourcemap_enabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F236
QUERIES: graph_model.Queries = ((FINDING, tsconfig_sourcemap_enabled),)
