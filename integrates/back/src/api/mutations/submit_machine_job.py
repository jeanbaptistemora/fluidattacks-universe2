from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from context import (
    PRODUCT_API_TOKEN,
)
from custom_types import (
    SimplePayload,
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
from skims_sdk import (
    get_finding_code_from_title,
    queue,
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
    finding = await info.context.loaders.finding.load(finding_id)
    group_name: str = finding["group_name"]

    root_nicknames: Set[str] = {
        root.nickname
        for root in await info.context.loaders.group_roots.load(group_name)
    }
    if root_nickname not in root_nicknames:
        return SimplePayload(success=False)

    finding_title: str = finding["title"]
    finding_code: Optional[str] = get_finding_code_from_title(finding_title)

    if finding_code is None:
        return SimplePayload(success=False)

    code, _, _ = await queue(
        finding_code=finding_code,
        group=group_name,
        namespace=root_nickname,
        product_api_token=PRODUCT_API_TOKEN,
        urgent=True,
    )

    return SimplePayload(success=code == 0)
