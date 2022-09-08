# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.subscriptions.enums import (
    SubscriptionEntity,
)


def translate_entity(entity: SubscriptionEntity) -> str:
    translation = {
        SubscriptionEntity.ORGANIZATION: "org",
    }
    if entity in translation:
        return translation[entity]
    return entity.lower()
