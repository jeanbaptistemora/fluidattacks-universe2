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
