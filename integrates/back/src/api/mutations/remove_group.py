from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    AlreadyPendingDeletion,
    PermissionDenied,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupStateJustification,
    GroupStateStatus,
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
)
from notifications import (
    domain as notifications_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@MUTATION.field("removeGroup")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    reason: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    requester_email = user_info["user_email"]
    group: Group = await loaders.group.load(group_name)
    if group.state.status == GroupStateStatus.DELETED:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Group {group_name} already in deleted state",
        )
        raise AlreadyPendingDeletion()

    try:
        await groups_domain.update_group(
            loaders=loaders,
            comments=kwargs.get("comments", ""),
            email=requester_email,
            group_name=group_name,
            justification=GroupStateJustification[reason.upper()],
            has_arm=False,
            has_machine=False,
            has_squad=False,
            service=group.state.service,
            subscription=group.state.type,
            tier=GroupTier.FREE,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted "
            f"to remove group {group_name}",
        )
        raise
    except APP_EXCEPTIONS as ex:
        await notifications_domain.delete_group(
            loaders=loaders,
            deletion_date=datetime_utils.get_utc_now(),
            group_name=group_name,
            requester_email=requester_email,
            reason=reason.upper(),
            comments=f"ARM exception: {ex}",
            attempt=None,
        )
        LOGGER.exception(
            "Error - could not remove group",
            extra={"extra": {"group_name": group_name, "ex": ex, **kwargs}},
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove group {group_name}, msg: {ex}",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed group {group_name} successfully",
    )

    return SimplePayload(success=True)
