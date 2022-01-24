from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f372.cloudformation import (
    cfn_elb2_uses_insecure_protocol,
    cfn_serves_content_over_http,
)
from lib_path.f372.terraform import (
    tfm_azure_kv_only_accessible_over_https,
    tfm_azure_sa_insecure_transfer,
    tfm_serves_content_over_http,
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
async def run_cfn_serves_content_over_http(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_serves_content_over_http,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_elb2_uses_insecure_protocol(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_elb2_uses_insecure_protocol,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_serves_content_over_http(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_serves_content_over_http,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_azure_kv_only_accessible_over_https(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_azure_kv_only_accessible_over_https,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_tfm_azure_sa_insecure_transfer(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_azure_sa_insecure_transfer,
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
                run_cfn_serves_content_over_http(content, path, template)
            )
            coroutines.append(
                run_cfn_elb2_uses_insecure_protocol(
                    content, file_extension, path, template
                )
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_tfm_serves_content_over_http(content, path, model)
        )
        coroutines.append(
            run_tfm_azure_kv_only_accessible_over_https(content, path, model)
        )
        coroutines.append(
            run_tfm_azure_sa_insecure_transfer(content, path, model)
        )

    return coroutines
