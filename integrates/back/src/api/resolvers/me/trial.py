from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from trials import (
    domain as trials_domain,
)
from typing import (
    Any,
)


@ME.field("trial")
async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any] | None:
    loaders: Dataloaders = info.context.loaders
    trial = await loaders.trial.load(parent["user_email"])

    if trial:
        return {
            "completed": trial.completed,
            "extension_date": trial.extension_date or "",
            "extension_days": trial.extension_days,
            "start_date": trial.start_date or "",
            "state": trials_domain.get_status(trial),
        }
    return None
