from lib_root.f024.cloudformation import (
    cfn_allows_anyone_to_admin_ports,
    cfn_ec2_has_open_all_ports_to_the_public,
    cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
    cfn_ec2_has_unrestricted_dns_access,
    cfn_ec2_has_unrestricted_ftp_access,
    cfn_ec2_has_unrestricted_ports,
    cfn_groups_without_egress,
    cfn_instances_without_profile,
    cfn_unrestricted_cidrs,
    cfn_unrestricted_ip_protocols,
)
from lib_root.f024.terraform import (
    tfm_aws_allows_anyone_to_admin_ports,
    tfm_aws_ec2_allows_all_outbound_traffic,
    tfm_aws_ec2_cfn_unrestricted_ip_protocols,
    tfm_aws_ec2_unrestricted_cidrs,
    tfm_ec2_has_open_all_ports_to_the_public,
    tfm_ec2_has_security_groups_ip_ranges_in_rfc1918,
    tfm_ec2_has_unrestricted_dns_access,
    tfm_ec2_has_unrestricted_ftp_access,
    tfm_ec2_has_unrestricted_ports,
    tfm_ec2_instances_without_profile,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F024
QUERIES: graph_model.Queries = (
    (FINDING, cfn_allows_anyone_to_admin_ports),
    (FINDING, cfn_ec2_has_open_all_ports_to_the_public),
    (FINDING, cfn_ec2_has_security_groups_ip_ranges_in_rfc1918),
    (FINDING, cfn_ec2_has_unrestricted_dns_access),
    (FINDING, cfn_ec2_has_unrestricted_ftp_access),
    (FINDING, cfn_ec2_has_unrestricted_ports),
    (FINDING, cfn_instances_without_profile),
    (FINDING, cfn_groups_without_egress),
    (FINDING, cfn_unrestricted_cidrs),
    (FINDING, cfn_unrestricted_ip_protocols),
    (FINDING, tfm_aws_allows_anyone_to_admin_ports),
    (FINDING, tfm_aws_ec2_allows_all_outbound_traffic),
    (FINDING, tfm_aws_ec2_cfn_unrestricted_ip_protocols),
    (FINDING, tfm_aws_ec2_unrestricted_cidrs),
    (FINDING, tfm_ec2_has_open_all_ports_to_the_public),
    (FINDING, tfm_ec2_has_security_groups_ip_ranges_in_rfc1918),
    (FINDING, tfm_ec2_has_unrestricted_dns_access),
    (FINDING, tfm_ec2_has_unrestricted_ftp_access),
    (FINDING, tfm_ec2_has_unrestricted_ports),
    (FINDING, tfm_ec2_instances_without_profile),
)
