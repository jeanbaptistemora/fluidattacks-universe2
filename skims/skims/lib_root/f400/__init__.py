from lib_root.f400.terraform import (
    tfm_distribution_has_logging_disabled,
    tfm_ec2_monitoring_disabled,
    tfm_elb_logging_disabled,
    tfm_lambda_tracing_disabled,
    tfm_trails_not_multiregion,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F400
QUERIES: graph_model.Queries = (
    (FINDING, tfm_distribution_has_logging_disabled),
    (FINDING, tfm_ec2_monitoring_disabled),
    (FINDING, tfm_elb_logging_disabled),
    (FINDING, tfm_lambda_tracing_disabled),
    (FINDING, tfm_trails_not_multiregion),
)
