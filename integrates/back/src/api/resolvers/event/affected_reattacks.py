from .schema import (
    EVENT,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("affectedReattacks")
async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Vulnerability]:
    event_id = parent.id
    loaders: Dataloaders = info.context.loaders

    return await loaders.event_vulnerabilities_loader.load(event_id)
