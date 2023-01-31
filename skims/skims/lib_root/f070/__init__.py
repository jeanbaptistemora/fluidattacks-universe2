from lib_root.f070.terraform import (
    tfm_elb2_uses_insecure_security_policy,
    tfm_lb_target_group_insecure_port,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F070
QUERIES: graph_model.Queries = (
    (FINDING, tfm_elb2_uses_insecure_security_policy),
    (FINDING, tfm_lb_target_group_insecure_port),
)
