from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    Any,
)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    frequency: str,
    report_entity: str,
    report_subject: str,
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders

    if await subscriptions_domain.can_subscribe_user_to_entity_report(
        loaders=loaders,
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    ):
        await subscriptions_domain.subscribe_user_to_entity_report(
            event_frequency=frequency,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"user: {user_email} edited subscription to "
            f"entity_report: {report_entity}/{report_subject} "
            f"frequency: {frequency}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"user: {user_email} attempted to edit subscription to "
            f"entity_report: {report_entity}/{report_subject} "
            f"frequency: {frequency} "
            f"without permission",
        )

    return SimplePayloadType(success=True)
