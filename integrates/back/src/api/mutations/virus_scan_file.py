from ariadne import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayload:
    files_data = parameters["files_data"]
    user_info = await token_utils.get_jwt_content(info.context)
    requester: str = parameters["group_name"]

    await put_action(
        action=Action.HANDLE_VIRUS_SCAN,
        entity=f"non_clients/{requester}",
        subject=user_info["user_email"],
        additional_info=files_data[0]["file_name"],
        queue="dedicated_soon",
        product_name=Product.INTEGRATES,
    )

    return SimplePayload(success=True)
