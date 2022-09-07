# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from typing import (
    NamedTuple,
)


class Subscription(NamedTuple):
    email: str
    entity: SubscriptionEntity
    frequency: SubscriptionFrequency
    subject: str
