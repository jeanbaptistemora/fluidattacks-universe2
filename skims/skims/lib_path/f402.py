from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
)
from parse_hcl2.common import (
    get_argument,
    get_block_attribute,
    get_block_block,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.azure import (
    iter_azurerm_storage_account,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)

_FINDING_F402 = core_model.FindingEnum.F402
_FINDING_F402_CWE = _FINDING_F402.value.cwe


def tfm_azure_storage_logging_disabled_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if queue_props := get_argument(
            key="queue_properties",
            body=resource.data,
        ):
            if logging_attr := get_block_block(queue_props, "logging"):
                attrs = [
                    get_block_attribute(logging_attr, req)
                    for req in ["delete", "read", "write"]
                ]
                if not all((req.val if req else False for req in attrs)):
                    yield logging_attr
            else:
                yield queue_props
        else:
            yield resource


def _tfm_azure_storage_logging_disabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F402_CWE},
        description_key="lib_path.f402.tfm_azure_storage_logging_disabled",
        finding=_FINDING_F402,
        iterator=get_cloud_iterator(
            tfm_azure_storage_logging_disabled_iterate_vulnerabilities(
                resource_iterator=iter_azurerm_storage_account(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_azure_storage_logging_disabled(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_azure_storage_logging_disabled,
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
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_azure_storage_logging_disabled(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
