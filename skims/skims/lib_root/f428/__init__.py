from lib_root.f428.conf_files import (
    unapropiated_comment as json_unapropiated_comment,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F428
QUERIES: graph_model.Queries = ((FINDING, json_unapropiated_comment),)
