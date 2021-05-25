from datetime import datetime
from functools import partial
from typing import Dict, List, Tuple

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from decorators import enforce_group_level_auth_async
from db_model.findings.types import Finding, FindingState
from newutils import datetime as datetime_utils
from redis_cluster.operations import redis_get_or_set_entity_attr


@enforce_group_level_auth_async
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Dict[str, str]]:
    response: List[Dict[str, str]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="historic_state_new",
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, str]]:
    historic_state_loader: DataLoader = (
        info.context.loaders.finding_historic_state_new
    )
    historic_state: Tuple[
        FindingState, ...
    ] = await historic_state_loader.load((parent.group_name, parent.id))
    return [
        {
            "analyst": state.modified_by,
            "date": datetime_utils.get_as_str(
                datetime.fromisoformat(state.modified_date)
            ),
            "source": state.source,
            "state": state.status.value,
        }
        for state in historic_state
    ]
