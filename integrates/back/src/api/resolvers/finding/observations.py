from .schema import (
    FINDING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
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


@FINDING.field("observations")
@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    observations: list[
        FindingComment
    ] = await comments_domain.get_observations(
        loaders, parent.group_name, parent.id, user_data["user_email"]
    )

    return [
        format_finding_consulting_resolve(comment) for comment in observations
    ]
