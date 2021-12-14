from aioextensions import (
    in_process,
)
from aws.model import (
    AWSElbV2,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
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
    iter_elb2_load_listeners,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
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
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F070 = core_model.FindingEnum.F070
_FINDING_F070_CWE = _FINDING_F070.value.cwe


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


def _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
    file_ext: str,
    listeners_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for listener in listeners_iterator:
        acceptable = (
            "ELBSecurityPolicy-2016-08",
            "ELBSecurityPolicy-TLS-1-1-2017-01",
            "ELBSecurityPolicy-FS-2018-06",
            "ELBSecurityPolicy-TLS-1-2-Ext-2018-06",
        )
        ssl_policy = listener.raw.get("SslPolicy", "")
        if ssl_policy not in acceptable:
            ssl_pol_node = get_node_by_keys(listener, ["SslPolicy"])
            if isinstance(ssl_pol_node, Node):
                yield ssl_pol_node
            else:
                yield AWSElbV2(
                    column=listener.start_column,
                    data=listener.data,
                    line=get_line_by_extension(listener.start_line, file_ext),
                )


def _tfm_lb_target_group_insecure_port(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F070_CWE},
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        finding=_FINDING_F070,
        iterator=get_cloud_iterator(
            tfm_lb_target_group_insecure_port_iterate_vulnerabilities(
                buckets_iterator=iter_aws_lb_target_group(model=model)
            )
        ),
        path=path,
    )


def _cfn_elb2_uses_insecure_security_policy(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F070_CWE},
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        finding=_FINDING_F070,
        iterator=get_cloud_iterator(
            _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
                file_ext=file_ext,
                listeners_iterator=iter_elb2_load_listeners(template=template),
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


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_elb2_uses_insecure_security_policy(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_elb2_uses_insecure_security_policy,
        content=content,
        file_ext=file_ext,
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
                cfn_elb2_uses_insecure_security_policy(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )
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
