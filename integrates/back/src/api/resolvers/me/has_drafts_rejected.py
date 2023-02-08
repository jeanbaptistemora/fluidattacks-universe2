from dataloaders import (
    Dataloaders,
)
from db_model.findings.utils import (
    has_rejected_drafts,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@require_login
async def resolve(parent: dict[str, Any], info: GraphQLResolveInfo) -> bool:
    loaders: Dataloaders = info.context.loaders
    email = str(parent["user_email"])
    drafts = await loaders.me_drafts.load(email)

    return has_rejected_drafts(drafts=drafts)
