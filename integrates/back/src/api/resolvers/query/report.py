from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
)
from custom_exceptions import (
    RequestedReportError,
)
from custom_types import (
    Report,
)
from decorators import (
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Dict,
)


@enforce_group_level_auth_async
async def _get_url_group_report(
    _info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    group_name: str,
) -> bool:
    success: bool = await batch_dal.put_action(
        action_name="report",
        entity=group_name,
        subject=user_email,
        additional_info=report_type,
    )
    if not success:
        raise RequestedReportError()
    return success


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Report:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = get_key_or_fallback(kwargs)
    report_type: str = kwargs["report_type"]
    return {
        "success": await _get_url_group_report(
            info,
            report_type,
            user_email,
            group_name=group_name,
        )
    }
