# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorSubscribingStakeholder,
)
from dataloaders import (
    Dataloaders,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from subscriptions import (
    domain as subscriptions_domain,
)


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
    subscription_frequency = SubscriptionFrequency[frequency.upper()]

    if not await subscriptions_domain.can_subscribe(
        loaders=loaders,
        entity=subscription_entity,
        subject=report_subject,
        email=email,
    ):
        logs_utils.cloudwatch_log(
            info.context,
            f"email: {email} attempted to edit subscription to "
            f"entity_report: {report_entity}/{report_subject} "
            f"frequency: {frequency} "
            f"without permission",
        )
        raise ErrorSubscribingStakeholder()

    await subscriptions_domain.subscribe(
        frequency=subscription_frequency,
        entity=subscription_entity,
        subject=report_subject,
        email=email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"email: {email} edited subscription to "
        f"entity_report: {report_entity}/{report_subject} "
        f"frequency: {frequency}",
    )

    return SimplePayloadType(success=True)
