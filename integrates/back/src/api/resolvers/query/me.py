from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
    Dict,
)


@QUERY.field("me")
@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Dict[str, Any]:
    caller_origin: str = kwargs.get("caller_origin", "API")
    user_data: Dict[str, Any] = await sessions_domain.get_jwt_content(
        info.context
    )
    exp: str = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_from_epoch(user_data["exp"])
    )
    return {
        "caller_origin": caller_origin,
        "session_expiration": exp,
        "user_email": user_data["user_email"],
        "user_name": " ".join(
            [user_data.get("first_name", ""), user_data.get("last_name", "")]
        ),
    }
