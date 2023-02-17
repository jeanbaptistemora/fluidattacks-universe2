from .schema import (
    FINDING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_as_str,
)


@FINDING.field("historicState")
@enforce_group_level_auth_async
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> list[dict[str, str]]:
    loaders: Dataloaders = info.context.loaders
    historic_state = await loaders.finding_historic_state.load(parent.id)

    return [
        {
            "analyst": state.modified_by,
            "date": get_as_str(state.modified_date),
            "source": str(state.source.value).lower(),
            "state": state.status.value,
        }
        for state in historic_state
    ]
