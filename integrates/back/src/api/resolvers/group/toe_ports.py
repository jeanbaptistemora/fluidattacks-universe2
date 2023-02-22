from .schema import (
    GROUP,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_ports.types import (
    GroupToePortsRequest,
    RootToePortsRequest,
    ToePortsConnection,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("toePorts")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(  # pylint: disable=too-many-arguments
    parent: Group,
    info: GraphQLResolveInfo,
    root_id: str | None = None,
    after: str | None = None,
    be_present: bool | None = None,
    first: int | None = None,
) -> ToePortsConnection:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    if root_id is not None:
        return await loaders.root_toe_ports.load(
            RootToePortsRequest(
                group_name=group_name,
                root_id=root_id,
                after=after,
                be_present=be_present,
                first=first,
                paginate=True,
            )
        )

    return await loaders.group_toe_ports.load(
        GroupToePortsRequest(
            group_name=group_name,
            after=after,
            be_present=be_present,
            first=first,
            paginate=True,
        )
    )
