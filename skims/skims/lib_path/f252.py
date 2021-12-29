from aioextensions import (
    in_process,
)
from aws.model import (
    AWSEC2,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
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

    return coroutines
