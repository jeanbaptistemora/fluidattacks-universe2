from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD,
)
from lib_path.f325.cloudformation import (
    cfn_iam_has_privileges_over_iam,
    cfn_iam_has_wildcard_resource_on_write_action,
    cfn_iam_is_policy_miss_configured,
    cfn_iam_is_role_over_privileged,
    cfn_kms_key_has_master_keys_exposed_to_everyone,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates,
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
async def run_cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_kms_key_has_master_keys_exposed_to_everyone,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_has_wildcard_resource_on_write_action,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_is_policy_miss_configured(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_is_policy_miss_configured,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_has_privileges_over_iam,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_is_role_over_privileged,
        content=content,
        file_ext=file_ext,
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
                run_cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_iam_has_wildcard_resource_on_write_action(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_iam_is_policy_miss_configured(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_iam_has_privileges_over_iam(content, path, template)
            )
            coroutines.append(
                run_cfn_iam_is_role_over_privileged(
                    content, file_extension, path, template
                )
            )

    return coroutines
