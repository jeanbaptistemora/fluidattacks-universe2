from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    get_vulnerabilities_from_aws_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_cloudtrail_trail,
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
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)


def _log_files_not_validated_iterate_vulnerabilities(
    trails_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    values = ["true", "True", True, "1", 1]
    for trail in trails_iterator:
        log_file_val = get_node_by_keys(trail, ["EnableLogFileValidation"])
        if isinstance(log_file_val, Node):
            if log_file_val.raw not in values:
                yield log_file_val
        else:
            yield trail


def _log_files_not_validated(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f091.cfn_log_files_not_validated",
        finding=core_model.FindingEnum.F091,
        path=path,
        statements_iterator=_log_files_not_validated_iterate_vulnerabilities(
            trails_iterator=iter_cloudtrail_trail(template=template)
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_log_files_not_validated(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _log_files_not_validated,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_log_files_not_validated(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
