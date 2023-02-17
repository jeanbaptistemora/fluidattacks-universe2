from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from finding_comments import (
    domain as comments_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.finding_comments import (
    format_finding_consulting_resolve,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@FINDING.field("consulting")
@concurrent_decorators(enforce_group_level_auth_async, require_asm)
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    user_data = await sessions_domain.get_jwt_content(info.context)
    finding_comments = await comments_domain.get_comments(
        loaders=info.context.loaders,
        group_name=parent.group_name,
        finding_id=parent.id,
        user_email=user_data["user_email"],
    )

    return [
        format_finding_consulting_resolve(comment)
        for comment in finding_comments
    ]
