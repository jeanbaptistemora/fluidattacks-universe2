from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f246.cloudformation import (
    cfn_rds_has_unencrypted_storage,
)
from lib_path.f246.terraform import (
    tfm_db_has_unencrypted_storage,
    tfm_rds_has_unencrypted_storage,
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
async def run_cfn_rds_has_unencrypted_storage(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_rds_has_unencrypted_storage,
        content=content,
        file_ext=file_ext,
        path=path,
        template=template,
    )


@SHIELD
@TIMEOUT_1MIN
async def run_tfm_rds_has_unencrypted_storage(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_rds_has_unencrypted_storage,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
@TIMEOUT_1MIN
async def run_tfm_db_has_unencrypted_storage(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_db_has_unencrypted_storage,
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
                run_cfn_rds_has_unencrypted_storage(
                    content, file_extension, path, template
                )
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_tfm_rds_has_unencrypted_storage(content, path, model)
        )
        coroutines.append(
            run_tfm_db_has_unencrypted_storage(content, path, model)
        )

    return coroutines
