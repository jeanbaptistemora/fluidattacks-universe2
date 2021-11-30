from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_aws_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    iter_aws_lb_target_group,
)
from parse_hcl2.tokens import (
    Attribute,
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
    TIMEOUT_1MIN,
)

FINDING_F070 = core_model.FindingEnum.F070
FINDING_F070_CWE = FINDING_F070.value.cwe


def tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "port"
                and elem.val != 443
            ):
                yield elem


def _tfm_lb_target_group_insecure_port(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FINDING_F070_CWE},
        description_key="F070.title",
        finding=FINDING_F070,
        iterator=get_aws_iterator(
            tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
                buckets_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_lb_target_group_insecure_port(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_lb_target_group_insecure_port,
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
            tfm_lb_target_group_insecure_port(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
