from lib_root.f396.terraform import (
    tfm_kms_key_is_key_rotation_absent_or_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F396
QUERIES: graph_model.Queries = (
    (FINDING, tfm_kms_key_is_key_rotation_absent_or_disabled),
)
