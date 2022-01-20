from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f177.cloudformation import (
    cfn_ec2_has_open_all_ports_to_the_public,
    cfn_ec2_has_unrestricted_dns_access,
    cfn_ec2_has_unrestricted_ftp_access,
    cfn_ec2_sg_allows_anyone_to_admin_ports,
)
from lib_path.f177.terraform import (
    ec2_use_default_security_group,
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
async def run_cfn_ec2_has_unrestricted_dns_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_unrestricted_dns_access,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_ec2_has_unrestricted_ftp_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_unrestricted_ftp_access,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_ec2_has_open_all_ports_to_the_public(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_open_all_ports_to_the_public,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_ec2_sg_allows_anyone_to_admin_ports(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_sg_allows_anyone_to_admin_ports,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_ec2_use_default_security_group(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        ec2_use_default_security_group,
        content=content,
        path=path,
        model=model,
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
                run_cfn_ec2_has_unrestricted_dns_access(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_ec2_has_unrestricted_ftp_access(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_ec2_has_open_all_ports_to_the_public(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_ec2_sg_allows_anyone_to_admin_ports(
                    content, path, template
                )
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_ec2_use_default_security_group(content, path, model)
        )

    return coroutines
