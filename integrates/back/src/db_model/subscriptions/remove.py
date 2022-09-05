from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_subscription"],
        values={
            "email": user_email,
            "entity": report_entity.lower(),
            "subject": report_subject,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
