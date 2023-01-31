from lib_root.f073.terraform import (
    tfm_db_instance_publicly_accessible,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
QUERIES: graph_model.Queries = (
    (FINDING, tfm_db_instance_publicly_accessible),
)
