from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from botocore.exceptions import (
    ClientError,
)
from contextlib import (
    suppress,
)
from custom_types import (
    SimplePayload,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRootItem,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_boto3,
)
from typing import (
    Optional,
    Set,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    root_nickname: str,
) -> SimplePayload:
    finding_loader = info.context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    group_name: str = finding.group_name
    finding_title: str = finding.title
    root_nicknames: Set[str] = {
        root.state.nickname
        for root in await info.context.loaders.group_roots.load(group_name)
        if isinstance(root, GitRootItem)
    }
    if root_nickname not in root_nicknames:
        return SimplePayload(success=False)

    finding_code: Optional[str] = get_finding_code_from_title(finding_title)

    if finding_code is None:
        return SimplePayload(success=False)
    success = False
    with suppress(ClientError):
        await queue_boto3(
            finding_code=finding_code,
            group=group_name,
            namespace=root_nickname,
        )
        success = True

    return SimplePayload(success=success)
