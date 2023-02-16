from lib_root.f024.terraform import (
    tfm_aws_allows_anyone_to_admin_ports,
    tfm_aws_ec2_allows_all_outbound_traffic,
    tfm_aws_ec2_cfn_unrestricted_ip_protocols,
    tfm_aws_ec2_unrestricted_cidrs,
    tfm_ec2_has_security_groups_ip_ranges_in_rfc1918,
    tfm_ec2_has_unrestricted_dns_access,
    tfm_ec2_has_unrestricted_ports,
    tfm_ec2_instances_without_profile,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F024
QUERIES: graph_model.Queries = (
    (FINDING, tfm_aws_allows_anyone_to_admin_ports),
    (FINDING, tfm_aws_ec2_allows_all_outbound_traffic),
    (FINDING, tfm_aws_ec2_cfn_unrestricted_ip_protocols),
    (FINDING, tfm_aws_ec2_unrestricted_cidrs),
    (FINDING, tfm_ec2_has_security_groups_ip_ranges_in_rfc1918),
    (FINDING, tfm_ec2_has_unrestricted_dns_access),
    (FINDING, tfm_ec2_has_unrestricted_ports),
    (FINDING, tfm_ec2_instances_without_profile),
)
