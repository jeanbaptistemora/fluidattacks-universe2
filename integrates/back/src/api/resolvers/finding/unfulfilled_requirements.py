from api.resolvers.types import (
    Requirement,
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


@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Requirement]:
    loaders: Dataloaders = info.context.loaders
    requirements_file = await loaders.requirements_file.load("")

    return [
        Requirement(
            id=requirement_id,
            title=requirements_file[requirement_id]["en"]["title"],
        )
        for requirement_id in parent.unfulfilled_requirements
    ]
