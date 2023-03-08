from lib_root.f400.cloudformation import (
    cfn_bucket_has_logging_conf_disabled,
    cfn_cf_distribution_has_logging_disabled,
    cfn_ec2_monitoring_disabled,
    cfn_elb2_has_access_logs_s3_disabled,
    cfn_elb_has_access_logging_disabled,
    cfn_trails_not_multiregion,
)
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
    (FINDING, cfn_bucket_has_logging_conf_disabled),
    (FINDING, cfn_cf_distribution_has_logging_disabled),
    (FINDING, cfn_ec2_monitoring_disabled),
    (FINDING, cfn_elb_has_access_logging_disabled),
    (FINDING, cfn_elb2_has_access_logs_s3_disabled),
    (FINDING, cfn_trails_not_multiregion),
    (FINDING, tfm_distribution_has_logging_disabled),
    (FINDING, tfm_ec2_monitoring_disabled),
    (FINDING, tfm_elb_logging_disabled),
    (FINDING, tfm_lambda_tracing_disabled),
    (FINDING, tfm_trails_not_multiregion),
)
