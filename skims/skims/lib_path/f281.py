from aioextensions import (
    in_process,
)
from aws.model import (
    AWSElbV2,
    AWSS3BucketPolicy,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    FALSE_OPTIONS,
    get_aws_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
    TRUE_OPTIONS,
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
    iter_elb2_load_target_groups,
    iter_s3_bucket_policies,
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

_FINDING_F281 = core_model.FindingEnum.F281
_FINDING_F281_CWE = _FINDING_F281.value.cwe


def _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
    policies_iterator: Iterator[Union[AWSS3BucketPolicy, Node]],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            secure_transport = get_node_by_keys(
                statement, ["Condition", "Bool", "aws:SecureTransport"]
            )
            if isinstance(secure_transport, Node) and (
                (effect == "Deny" and secure_transport.raw in TRUE_OPTIONS)
                or (
                    effect == "Allow" and secure_transport.raw in FALSE_OPTIONS
                )
            ):
                yield secure_transport


def _cfn_elb2_uses_insecure_port_iterate_vulnerabilities(
    file_ext: str,
    t_groups_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for t_group in t_groups_iterator:
        safe_ports = (443,)
        port = t_group.raw.get("Port", 80)
        is_port_required = t_group.raw.get("TargetType", "")
        if is_port_required and port not in safe_ports:
            port_node = get_node_by_keys(t_group, ["Port"])
            if isinstance(port_node, Node):
                yield port_node
            else:
                yield AWSElbV2(
                    column=t_group.start_column,
                    data=t_group.data,
                    line=get_line_by_extension(t_group.start_line, file_ext),
                )


def _cfn_bucket_policy_has_secure_transport(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F281_CWE},
        description_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        finding=_FINDING_F281,
        iterator=get_aws_iterator(
            _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
    )


def _cfn_elb2_uses_insecure_port(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F281_CWE},
        description_key="src.lib_path.f281.elb2_uses_insecure_port",
        finding=_FINDING_F281,
        iterator=get_aws_iterator(
            _cfn_elb2_uses_insecure_port_iterate_vulnerabilities(
                file_ext=file_ext,
                t_groups_iterator=iter_elb2_load_target_groups(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_bucket_policy_has_secure_transport(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_bucket_policy_has_secure_transport,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_elb2_uses_insecure_port(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_elb2_uses_insecure_port,
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
                cfn_bucket_policy_has_secure_transport(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
