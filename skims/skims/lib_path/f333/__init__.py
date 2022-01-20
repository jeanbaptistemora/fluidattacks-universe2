from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f333.cloudformation import (
    cfn_ec2_has_not_an_iam_instance_profile,
    cfn_iam_has_full_access_to_ssm,
)
from lib_path.f333.terraform import (
    ec2_has_not_termination_protection,
    ec2_has_terminate_shutdown_behavior,
    tfm_ec2_associate_public_ip_address,
    tfm_ec2_has_not_an_iam_instance_profile,
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
async def run_cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_ec2_has_not_an_iam_instance_profile,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_has_full_access_to_ssm,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_ec2_has_terminate_shutdown_behavior(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        ec2_has_terminate_shutdown_behavior,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_ec2_has_not_termination_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        ec2_has_not_termination_protection,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_ec2_has_not_an_iam_instance_profile(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_ec2_has_not_an_iam_instance_profile,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_ec2_associate_public_ip_address(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_ec2_associate_public_ip_address,
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
                run_cfn_ec2_has_not_an_iam_instance_profile(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_iam_has_full_access_to_ssm(content, path, template)
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_ec2_has_terminate_shutdown_behavior(content, path, model)
        )
        coroutines.append(
            run_ec2_has_not_termination_protection(content, path, model)
        )
        coroutines.append(
            run_tfm_ec2_has_not_an_iam_instance_profile(content, path, model)
        )
        coroutines.append(
            run_tfm_ec2_associate_public_ip_address(content, path, model)
        )

    return coroutines
