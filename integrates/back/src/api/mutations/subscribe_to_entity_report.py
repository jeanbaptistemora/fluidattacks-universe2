# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
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

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    frequency: str,
    report_entity: str,
    report_subject: str,
) -> SimplePayloadType:
    loaders: Dataloaders = info.context.loaders
    user_info = await token_utils.get_jwt_content(info.context)
    email = user_info["user_email"]
    subscription_entity = SubscriptionEntity[report_entity.upper()]

    if await subscriptions_domain.can_subscribe(
        loaders=loaders,
        entity=subscription_entity,
        subject=report_subject,
        email=email,
    ):
        await subscriptions_domain.subscribe_user_to_entity_report(
            event_frequency=frequency,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=email,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"user: {email} edited subscription to "
            f"entity_report: {report_entity}/{report_subject} "
            f"frequency: {frequency}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"user: {email} attempted to edit subscription to "
            f"entity_report: {report_entity}/{report_subject} "
            f"frequency: {frequency} "
            f"without permission",
        )

    return SimplePayloadType(success=True)
