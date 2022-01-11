from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
    AWSEC2Rule,
)
from itertools import (
    chain,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
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
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
)
from parse_hcl2.common import (
    get_argument,
    get_attribute,
    get_block_attribute,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iter_aws_security_group,
    iter_aws_security_group_rule,
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

_FINDING_F252 = core_model.FindingEnum.F252
_FINDING_F252_CWE = _FINDING_F252.value.cwe


def _cfn_ec2_has_unrestricted_ports_iterate_vulnerabilities(
    ec2_iterator: Iterator[Union[AWSEC2, Node]],
) -> Iterator[Union[AWSEC2, Node]]:
    for ec2_res in ec2_iterator:
        from_port = ec2_res.inner.get("FromPort")
        to_port = ec2_res.inner.get("ToPort")
        if (
            from_port
            and to_port
            and float(from_port.raw) != float(to_port.raw)
        ):
            yield from_port


def tfm_ec2_has_unrestricted_ports_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Any]:
    for resource in resource_iterator:
        if isinstance(resource, AWSEC2):
            if ingress_block := get_argument(
                key="ingress",
                body=resource.data,
            ):
                ingress_from_port = get_block_attribute(
                    block=ingress_block, key="from_port"
                )
                ingress_to_port = get_block_attribute(
                    block=ingress_block, key="to_port"
                )
                if (
                    ingress_from_port
                    and ingress_to_port
                    and float(ingress_from_port.val)
                    != float(ingress_to_port.val)
                ):
                    yield ingress_block
            if egress_block := get_argument(
                key="egress",
                body=resource.data,
            ):
                egress_from_port = get_block_attribute(
                    block=egress_block, key="from_port"
                )
                egress_to_port = get_block_attribute(
                    block=egress_block, key="to_port"
                )
                if (
                    egress_from_port
                    and egress_to_port
                    and float(egress_from_port.val)
                    != float(egress_to_port.val)
                ):
                    yield egress_block
        elif isinstance(resource, AWSEC2Rule):
            from_port_attr = get_attribute(body=resource.data, key="from_port")
            to_port_attr = get_attribute(body=resource.data, key="to_port")
            if (
                from_port_attr
                and to_port_attr
                and float(from_port_attr.val) != float(to_port_attr.val)
            ):
                yield resource


def _cfn_ec2_has_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F252_CWE},
        description_key=("src.lib_path.f252.ec2_has_unrestricted_ports"),
        finding=_FINDING_F252,
        iterator=get_cloud_iterator(
            _cfn_ec2_has_unrestricted_ports_iterate_vulnerabilities(
                ec2_iterator=iter_ec2_ingress_egress(
                    template=template, ingress=True, egress=True
                ),
            )
        ),
        path=path,
    )


def _tfm_ec2_has_unrestricted_ports(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F252_CWE},
        description_key="src.lib_path.f252.ec2_has_unrestricted_ports",
        finding=_FINDING_F252,
        iterator=get_cloud_iterator(
            tfm_ec2_has_unrestricted_ports_iterate_vulnerabilities(
                resource_iterator=chain(
                    iter_aws_security_group(model=model),
                    iter_aws_security_group_rule(model=model),
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_ec2_has_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_ec2_has_unrestricted_ports,
        content=content,
        path=path,
        template=template,
    )


#  @CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def tfm_ec2_has_unrestricted_ports(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_ec2_has_unrestricted_ports,
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
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_ec2_has_unrestricted_ports(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_ec2_has_unrestricted_ports(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
