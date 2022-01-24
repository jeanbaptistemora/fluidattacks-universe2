from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f401.terraform import (
    tfm_azure_kv_secret_no_expiration_date,
)
from model.core_model import (
    Vulnerabilities,
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
async def run_tfm_azure_kv_secret_no_expiration_date(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return await in_process(
        tfm_azure_kv_secret_no_expiration_date,
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

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_tfm_azure_kv_secret_no_expiration_date(content, path, model)
        )

    return coroutines
