from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f024.cloudformation import (
    cfn_allows_anyone_to_admin_ports,
    cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
    cfn_ec2_has_unrestricted_ports,
    cfn_groups_without_egress,
    cfn_instances_without_profile,
    cfn_unrestricted_cidrs,
    cfn_unrestricted_ip_protocols,
    cfn_unrestricted_ports,
)
from lib_path.f024.terraform import (
    tfm_aws_ec2_allows_all_outbound_traffic,
    tfm_aws_ec2_cfn_unrestricted_ip_protocols,
    tfm_aws_ec2_unrestricted_cidrs,
    tfm_ec2_has_unrestricted_ports,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_instances_without_profile(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_instances_without_profile,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_unrestricted_cidrs(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W2 Security Groups found with cidr open to world on ingress
    # cfn_nag W5 Security Groups found with cidr open to world on egress
    # cfn_nag W9 Security Groups found with ingress cidr that is not /32
    return await in_process(
        cfn_unrestricted_cidrs,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_unrestricted_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W27 Security Groups found ingress with port range instead of just
    # a single port
    # cfn_nag W29 Security Groups found egress with port range instead of just
    # a single port
    return await in_process(
        cfn_unrestricted_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_allows_anyone_to_admin_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_allows_anyone_to_admin_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_unrestricted_ip_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W40 Security Groups egress with an IpProtocol of -1 found
    # cfn_nag W42 Security Groups ingress with an ipProtocol of -1 found
    return await in_process(
        cfn_unrestricted_ip_protocols,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_security_groups_ip_ranges_in_rfc1918,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_ec2_has_unrestricted_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_unrestricted_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_aws_ec2_allows_all_outbound_traffic(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_aws_ec2_allows_all_outbound_traffic,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_aws_ec2_cfn_unrestricted_ip_protocols,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_aws_ec2_unrestricted_cidrs(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_aws_ec2_unrestricted_cidrs,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_ec2_has_unrestricted_ports(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_ec2_has_unrestricted_ports,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_groups_without_egress(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag F1000 Missing egress rule means all traffic is allowed outbound
    return await in_process(
        cfn_groups_without_egress,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:

    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        async for template in load_templates(content, fmt=file_extension):
            coroutines.append(
                run_cfn_instances_without_profile(content, path, template)
            )
            coroutines.append(
                run_cfn_unrestricted_cidrs(content, path, template)
            )
            coroutines.append(
                run_cfn_unrestricted_ports(content, path, template)
            )
            coroutines.append(
                run_cfn_allows_anyone_to_admin_ports(content, path, template)
            )
            coroutines.append(
                run_cfn_unrestricted_ip_protocols(content, path, template)
            )
            coroutines.append(
                run_cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_ec2_has_unrestricted_ports(content, path, template)
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_tfm_aws_ec2_allows_all_outbound_traffic(content, path, model)
        )
        coroutines.append(
            run_tfm_aws_ec2_cfn_unrestricted_ip_protocols(content, path, model)
        )
        coroutines.append(
            run_tfm_aws_ec2_unrestricted_cidrs(content, path, model)
        )
        coroutines.append(
            run_tfm_ec2_has_unrestricted_ports(content, path, model)
        )

    return coroutines
