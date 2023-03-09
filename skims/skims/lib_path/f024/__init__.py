from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f024.cloudformation import (
    cfn_allows_anyone_to_admin_ports,
    cfn_ec2_has_open_all_ports_to_the_public,
    cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
    cfn_unrestricted_cidrs,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


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


@SHIELD_BLOCKING
def run_cfn_allows_anyone_to_admin_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_allows_anyone_to_admin_ports(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
        content=content, path=path, template=template
    )


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
) -> tuple[Vulnerabilities, ...]:

    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                *(
                    fun(content, path, template)
                    for fun in (
                        run_cfn_unrestricted_cidrs,
                        run_cfn_allows_anyone_to_admin_ports,
                        run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
                        run_cfn_ec2_has_open_all_ports_to_the_public,
                    )
                ),
            )

    return results
