from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f400.cloudformation import (
    cfn_bucket_has_logging_conf_disabled,
    cfn_cf_distribution_has_logging_disabled,
    cfn_elb2_has_access_logs_s3_disabled,
    cfn_elb_has_access_logging_disabled,
    cfn_trails_not_multiregion,
)
from lib_path.f400.terraform import (
    tfm_elb_logging_disabled,
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
async def run_cfn_bucket_has_logging_conf_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_bucket_has_logging_conf_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_elb_has_access_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_elb_has_access_logging_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_cf_distribution_has_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_cf_distribution_has_logging_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_trails_not_multiregion(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_trails_not_multiregion,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_elb2_has_access_logs_s3_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_elb2_has_access_logs_s3_disabled,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_elb_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_elb_logging_disabled,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        async for template in load_templates(content, fmt=file_extension):
            coroutines.append(
                run_cfn_bucket_has_logging_conf_disabled(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_elb_has_access_logging_disabled(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_cf_distribution_has_logging_disabled(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_trails_not_multiregion(
                    content, file_extension, path, template
                )
            )
            coroutines.append(
                run_cfn_elb2_has_access_logs_s3_disabled(
                    content, file_extension, path, template
                )
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(run_tfm_elb_logging_disabled(content, path, model))

    return coroutines
