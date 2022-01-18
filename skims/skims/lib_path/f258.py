from aioextensions import (
    in_process,
)
from aws.model import (
    AWSElbV2,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
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
    iter_elb2_load_balancers,
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

_FINDING_F258 = core_model.FindingEnum.F258
_FINDING_F258_CWE = _FINDING_F258.value.cwe


def _cfn_elb2_has_not_deletion_protection_iterate_vulnerabilities(
    file_ext: str,
    load_balancers_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for elb in load_balancers_iterator:
        attrs = get_node_by_keys(elb, ["LoadBalancerAttributes"])
        if not isinstance(attrs, Node):
            yield AWSElbV2(
                column=elb.start_column,
                data=elb.data,
                line=get_line_by_extension(elb.start_line, file_ext),
            )
        else:
            key_vals = [
                attr
                for attr in attrs.data
                if attr.raw["Key"] == "deletion_protection.enabled"
            ]
            if key_vals:
                key = key_vals[0]
                if key.raw["Value"] in FALSE_OPTIONS:
                    yield key.inner["Value"]
            else:
                yield AWSElbV2(
                    column=attrs.start_column,
                    data=attrs.data,
                    line=get_line_by_extension(attrs.start_line, file_ext),
                )


def _cfn_elb2_has_not_deletion_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F258_CWE},
        description_key="src.lib_path.f258.elb2_has_not_deletion_protection",
        finding=_FINDING_F258,
        iterator=get_cloud_iterator(
            _cfn_elb2_has_not_deletion_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                load_balancers_iterator=iter_elb2_load_balancers(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_elb2_has_not_deletion_protection(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_elb2_has_not_deletion_protection,
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
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_elb2_has_not_deletion_protection(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )

    return coroutines
