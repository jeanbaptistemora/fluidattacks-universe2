from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from context import (
    FI_API_STATUS,
    PRODUCT_API_TOKEN,
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
    if FI_API_STATUS == "migration":
        finding_new_loader = info.context.loaders.finding_new
        finding: Finding = await finding_new_loader.load(finding_id)
        group_name: str = finding.group_name
        finding_title: str = finding.title
    else:
        finding = await info.context.loaders.finding.load(finding_id)
        group_name = finding["group_name"]
        finding_title = finding["title"]

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

    code, _, _ = await queue(
        finding_code=finding_code,
        group=group_name,
        namespace=root_nickname,
        product_api_token=PRODUCT_API_TOKEN,
        urgent=True,
    )

    return SimplePayload(success=code == 0)
