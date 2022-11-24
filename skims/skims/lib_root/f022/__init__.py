from lib_root.f022.kotlin import (
    unencrypted_channel as kotlin_unencrypted_channel,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F022
QUERIES: graph_model.Queries = ((FINDING, kotlin_unencrypted_channel),)
