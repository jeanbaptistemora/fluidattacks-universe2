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
    iter_aws_instance,
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

_FINDING_F177 = core_model.FindingEnum.F177
_FINDING_F177_CWE = _FINDING_F177.value.cwe

SECURITY_GROUP_ATTRIBUTES = {"security_groups", "vpc_security_group_ids"}


def ec2_use_default_security_group_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        use_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key in SECURITY_GROUP_ATTRIBUTES
            ):
                use_attr = True
        if not use_attr:
            yield bucket


def aws_instance_use_default_security_group_iterate_vulnerabilities(
    buckets_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for bucket in buckets_iterator:
        use_attr = False
        for elem in bucket.data:
            if (
                isinstance(elem, Attribute)
                and elem.key in SECURITY_GROUP_ATTRIBUTES
            ):
                use_attr = True
        if not use_attr:
            yield bucket


def _ec2_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key="F177.title",
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            ec2_use_default_security_group_iterate_vulnerabilities(
                buckets_iterator=iter_aws_launch_template(model=model)
            )
        ),
        path=path,
    )


def _aws_instance_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key="F177.title",
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            aws_instance_use_default_security_group_iterate_vulnerabilities(
                buckets_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def ec2_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _ec2_use_default_security_group,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
@TIMEOUT_1MIN
async def aws_instance_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _aws_instance_use_default_security_group,
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
            ec2_use_default_security_group(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            aws_instance_use_default_security_group(
                content=content,
                path=path,
                model=model,
            )
        )
    return coroutines
