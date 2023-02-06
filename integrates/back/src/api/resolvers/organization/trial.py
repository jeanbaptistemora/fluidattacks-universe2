from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from trials import (
    domain as trials_domain,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    trial = await loaders.trial.load(parent.created_by)

    if trial:
        return {
            "completed": trial.completed,
            "extension_date": trial.extension_date or "",
            "extension_days": trial.extension_days,
            "start_date": trial.start_date or "",
            "state": trials_domain.get_status(trial),
        }
    return None
