from lib_root.f016.c_sharp import (
    httpclient_no_revocation_list as c_sharp_httpclient_no_revocation_list,
    insecure_shared_access_protocol as c_sharp_insecure_shared_access_protocol,
    service_point_manager_disabled as c_sharp_service_point_manager_disabled,
    weak_protocol as c_sharp_weak_protocol,
)
from lib_root.f016.cloudformation import (
    cfn_elb_without_sslpolicy,
    cfn_serves_content_over_insecure_protocols,
)
from lib_root.f016.terraform import (
    tfm_aws_elb_without_sslpolicy,
    tfm_aws_serves_content_over_insecure_protocols,
    tfm_azure_serves_content_over_insecure_protocols,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F016
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_weak_protocol),
    (FINDING, c_sharp_service_point_manager_disabled),
    (FINDING, c_sharp_insecure_shared_access_protocol),
    (FINDING, c_sharp_httpclient_no_revocation_list),
    (FINDING, cfn_elb_without_sslpolicy),
    (FINDING, cfn_serves_content_over_insecure_protocols),
    (FINDING, tfm_aws_elb_without_sslpolicy),
    (FINDING, tfm_aws_serves_content_over_insecure_protocols),
    (FINDING, tfm_azure_serves_content_over_insecure_protocols),
)
