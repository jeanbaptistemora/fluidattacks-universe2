from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidBePresentFilterCursor,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    RootToeInputsRequest,
    ToeInputsConnection,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    validate_connection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(  # pylint: disable=too-many-arguments
    parent: Group,
    info: GraphQLResolveInfo,
    root_id: Optional[str] = None,
    after: Optional[str] = None,
    be_present: Optional[bool] = None,
    first: Optional[int] = None,
) -> Optional[ToeInputsConnection]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    if root_id is not None:
        response: Optional[
            ToeInputsConnection
        ] = await loaders.root_toe_inputs.load(
            RootToeInputsRequest(
                group_name=group_name,
                root_id=root_id,
                after=after,
                be_present=be_present,
                first=first,
                paginate=True,
            )
        )
        if response:
            return response
        raise InvalidBePresentFilterCursor()

    response = await loaders.group_toe_inputs.load(
        GroupToeInputsRequest(
            group_name=group_name,
            after=after,
            be_present=be_present,
            first=first,
            paginate=True,
        )
    )
    return response
