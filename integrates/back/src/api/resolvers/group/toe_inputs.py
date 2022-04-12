from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
    Any,
    Dict,
    Optional,
    Union,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    validate_connection,
)
async def resolve(  # pylint: disable=too-many-arguments
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    root_id: Optional[str] = None,
    after: Optional[str] = None,
    be_present: Optional[bool] = None,
    first: Optional[int] = None,
) -> ToeInputsConnection:
    loaders: Dataloaders = info.context.loaders
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    if root_id is not None:
        response: ToeInputsConnection = await loaders.root_toe_inputs.load(
            RootToeInputsRequest(
                group_name=group_name,
                root_id=root_id,
                after=after,
                be_present=be_present,
                first=first,
                paginate=True,
            )
        )
        return response

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
