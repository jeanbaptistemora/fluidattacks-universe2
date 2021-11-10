from aioextensions import (
    in_process,
)
from aws.model import (
    AWSS3BucketPolicy,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    FALSE_OPTIONS,
    get_vulnerabilities_from_aws_iterator_blocking,
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


def _cfn_bucket_policy_has_secure_transport(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        finding=core_model.FindingEnum.F281,
        path=path,
        statements_iterator=(
            _cfn_bucket_policy_has_secure_transport_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
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
