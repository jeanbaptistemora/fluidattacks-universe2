from lib_root.f250.terraform import (
    tfm_ebs_unencrypted_by_default,
    tfm_ebs_unencrypted_volumes,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F250
QUERIES: graph_model.Queries = (
    (FINDING, tfm_ebs_unencrypted_by_default),
    (FINDING, tfm_ebs_unencrypted_volumes),
)
