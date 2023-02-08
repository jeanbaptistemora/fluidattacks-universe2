from lib_root.f400.terraform import (
    tfm_ec2_monitoring_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F400
QUERIES: graph_model.Queries = ((FINDING, tfm_ec2_monitoring_disabled),)
