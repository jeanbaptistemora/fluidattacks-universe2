from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
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
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
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


def _cfn_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        cidr = ec2_res.raw.get("CidrIp", None) or ec2_res.raw.get(
            "CidrIpv6", None
        )
        is_public_cidr = cidr in (
            "::/0",
            "0.0.0.0/0",
        )
        if not is_public_cidr:
            continue
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if (
            from_port
            and to_port
            and float(from_port.raw) <= 53 <= float(to_port.raw)
        ):
            yield from_port


def _ec2_use_default_security_group(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key="lib_path.f177.ec2_using_default_security_group",
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
        description_key="lib_path.f177.ec2_using_default_security_group",
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            aws_instance_use_default_security_group_iterate_vulnerabilities(
                buckets_iterator=iter_aws_instance(model=model)
            )
        ),
        path=path,
    )


def _cfn_ec2_has_unrestricted_dns_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F177_CWE},
        description_key=("src.lib_path.f177.ec2_has_unrestricted_dns_access"),
        finding=_FINDING_F177,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_dns_access_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
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


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_dns_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_dns_access,
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
