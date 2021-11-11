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


def _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
    policies_iterator: Iterator[Union[AWSS3BucketPolicy, Node]],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            sse = get_node_by_keys(
                statement,
                ["Condition", "Null", "s3:x-amz-server-side-encryption"],
            )
            if isinstance(sse, Node) and (
                effect == "Allow" and sse.raw in FALSE_OPTIONS
            ):
                yield sse


def _cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f099.bckp_has_server_side_encryption_disabled"
        ),
        finding=core_model.FindingEnum.F099,
        path=path,
        statements_iterator=(
            _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_bucket_policy_has_server_side_encryption_disabled,
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
                cfn_bucket_policy_has_server_side_encryption_disabled(
                    content=content,
                    path=path,
                    template=template,
                )
            )

    return coroutines
