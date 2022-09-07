# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(
    *,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_subscription"],
        values={
            "email": email,
            "entity": entity.lower(),
            "subject": subject,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
