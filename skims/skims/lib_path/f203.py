from aioextensions import (
    in_process,
)
from aws.model import (
    AWSS3Bucket,
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
    iter_s3_buckets,
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


def cfn_has_not_private_access_control_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSS3Bucket, Node]],
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for bucket in buckets_iterator:
        access_control = get_node_by_keys(bucket, ["AccessControl"])
        if (
            isinstance(access_control, Node)
            and access_control.raw != "Private"
        ):
            yield access_control


def _cfn_has_not_private_access_control(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f203.cfn_has_not_private_access_control",
        finding=core_model.FindingEnum.F203,
        path=path,
        statements_iterator=(
            cfn_has_not_private_access_control_iterate_vulnerabilities(
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_has_not_private_access_control(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_has_not_private_access_control,
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
                cfn_has_not_private_access_control(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
