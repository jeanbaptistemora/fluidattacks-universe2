from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    get_cloud_iterator,
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
from parse_hcl2.structure.aws import (
    iter_aws_launch_template,
)
from parse_hcl2.tokens import (
    Attribute,
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

_FINDING_F333 = core_model.FindingEnum.F333
_FINDING_F333_CWE = _FINDING_F333.value.cwe


def ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "instance_initiated_shutdown_behavior"
                and isinstance(elem.val, str)
                and elem.val.lower() != "terminate"
            ):
                yield elem


def ec2_has_not_termination_protection_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        protection_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key == "disable_api_termination"
            ):
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield bucket


def _ec2_has_terminate_shutdown_behavior(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="lib_path.f333.ec2_allows_shutdown_command",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            ec2_has_terminate_shutdown_behavior_iterate_vulnerabilities(
                buckets_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


def _ec2_has_not_termination_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F333_CWE},
        description_key="F333.title",
        finding=_FINDING_F333,
        iterator=get_cloud_iterator(
            ec2_has_not_termination_protection_iterate_vulnerabilities(
                buckets_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def ec2_has_terminate_shutdown_behavior(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_has_terminate_shutdown_behavior,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
@TIMEOUT_1MIN
async def ec2_has_not_termination_protection(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_has_not_termination_protection,
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
            ec2_has_terminate_shutdown_behavior(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            ec2_has_not_termination_protection(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
