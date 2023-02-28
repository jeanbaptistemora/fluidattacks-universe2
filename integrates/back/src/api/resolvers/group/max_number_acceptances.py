from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from vulnerabilities.domain.validations import (
    get_policy_max_number_acceptances,
)


@GROUP.field("maxNumberAcceptances")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int | None:
    return await get_policy_max_number_acceptances(
        loaders=info.context.loaders, group_name=parent.name
    )
