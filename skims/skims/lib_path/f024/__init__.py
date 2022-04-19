from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f024.cloudformation import (
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
from lib_path.f024.terraform import (
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
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_instances_without_profile(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_instances_without_profile(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_unrestricted_cidrs(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W2 Security Groups found with cidr open to world on ingress
    # cfn_nag W5 Security Groups found with cidr open to world on egress
    # cfn_nag W9 Security Groups found with ingress cidr that is not /32
    return cfn_unrestricted_cidrs(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_allows_anyone_to_admin_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_allows_anyone_to_admin_ports(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_unrestricted_ip_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W40 Security Groups egress with an IpProtocol of -1 found
    # cfn_nag W42 Security Groups ingress with an ipProtocol of -1 found
    return cfn_unrestricted_ip_protocols(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_unrestricted_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_unrestricted_ports(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_ec2_allows_all_outbound_traffic(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_ec2_allows_all_outbound_traffic(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_ec2_cfn_unrestricted_ip_protocols(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_ec2_unrestricted_cidrs(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_ec2_unrestricted_cidrs(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_unrestricted_ports(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_unrestricted_ports(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_allows_anyone_to_admin_ports(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_allows_anyone_to_admin_ports(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_security_groups_ip_ranges_in_rfc1918(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_unrestricted_dns_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_unrestricted_dns_access(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_unrestricted_ftp_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_unrestricted_ftp_access(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_instances_without_profile(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_instances_without_profile(
        content=content, path=path, model=model
    )


# @CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_open_all_ports_to_the_public(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_open_all_ports_to_the_public(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_groups_without_egress(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag F1000 Missing egress rule means all traffic is allowed outbound
    return cfn_groups_without_egress(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_unrestricted_dns_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_unrestricted_dns_access(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_unrestricted_ftp_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_unrestricted_ftp_access(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_open_all_ports_to_the_public(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_open_all_ports_to_the_public(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                *(
                    fun(content, path, template)
                    for fun in (
                        run_cfn_instances_without_profile,
                        run_cfn_unrestricted_cidrs,
                        run_cfn_allows_anyone_to_admin_ports,
                        run_cfn_unrestricted_ip_protocols,
                        run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
                        run_cfn_ec2_has_unrestricted_ports,
                        run_cfn_ec2_has_unrestricted_dns_access,
                        run_cfn_ec2_has_unrestricted_ftp_access,
                        run_cfn_ec2_has_open_all_ports_to_the_public,
                        run_cfn_groups_without_egress,
                    )
                ),
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (
                    run_tfm_aws_allows_anyone_to_admin_ports,
                    run_tfm_ec2_has_security_groups_ip_ranges_in_rfc1918,
                    run_tfm_aws_ec2_allows_all_outbound_traffic,
                    run_tfm_aws_ec2_cfn_unrestricted_ip_protocols,
                    run_tfm_aws_ec2_unrestricted_cidrs,
                    run_tfm_ec2_has_unrestricted_ports,
                    run_tfm_ec2_has_unrestricted_dns_access,
                    run_tfm_ec2_has_unrestricted_ftp_access,
                    run_tfm_ec2_instances_without_profile,
                    run_tfm_ec2_has_open_all_ports_to_the_public,
                )
            ),
        )

    return results
