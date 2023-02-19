from api.mutations import (
    UpdateToeLinesPayload,
)
from ariadne import (
    ObjectType,
)
from custom_exceptions import (
    ToeLinesNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)

UPDATE_TOE_LINES_PAYLOAD = ObjectType("UpdateToeLinesPayload")


@UPDATE_TOE_LINES_PAYLOAD.field("toeLines")
async def resolve(
    parent: UpdateToeLinesPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> ToeLines:
    loaders: Dataloaders = info.context.loaders
    request = ToeLinesRequest(
        filename=parent.filename,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_lines.clear(request)
    toe_lines = await loaders.toe_lines.load(request)
    if toe_lines is None:
        raise ToeLinesNotFound()

    return toe_lines
