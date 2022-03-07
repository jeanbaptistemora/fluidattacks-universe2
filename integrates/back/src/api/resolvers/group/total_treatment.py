from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import simplejson as json  # type: ignore
from typing import (
    Any,
    Dict,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> object:
    if isinstance(parent, dict):
        total_treatment: Dict[str, int] = parent.get("total_treatment", {})
    else:
        loaders: Dataloaders = info.context.loaders
        group_name: str = parent.name
        group_indicators: GroupUnreliableIndicators = (
            await loaders.group_indicators_typed.load(group_name)
        )
        total_treatment = (
            group_indicators.treatment_summary._asdict()
            if group_indicators.treatment_summary
            else {}
        )

    return json.dumps(total_treatment, use_decimal=True)
