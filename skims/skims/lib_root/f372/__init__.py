from lib_root.f372.cloudformation import (
    cfn_elb2_uses_insecure_protocol,
)
from lib_root.f372.conf_files import (
    https_flag_missing as json_https_flag_missing,
)
from lib_root.f372.terraform import (
    tfm_aws_sec_group_using_http,
    tfm_azure_kv_only_accessible_over_https,
    tfm_azure_sa_insecure_transfer,
    tfm_elb2_uses_insecure_protocol,
    tfm_serves_content_over_http,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F372
QUERIES: graph_model.Queries = (
    (FINDING, cfn_elb2_uses_insecure_protocol),
    (FINDING, json_https_flag_missing),
    (FINDING, tfm_aws_sec_group_using_http),
    (FINDING, tfm_azure_kv_only_accessible_over_https),
    (FINDING, tfm_azure_sa_insecure_transfer),
    (FINDING, tfm_elb2_uses_insecure_protocol),
    (FINDING, tfm_serves_content_over_http),
)
