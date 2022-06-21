from .types import (
    NotificationsPreferences,
    Stakeholder,
)
from .utils import (
    format_stakeholder,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_stakeholder(*, stakeholder_email: str) -> Stakeholder:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": stakeholder_email},
    )

    item = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )

    if item:
        return format_stakeholder(item)

    return Stakeholder(
        email="",
        notifications_preferences=NotificationsPreferences(email=[]),
    )


class StakeholderLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: tuple[str, ...]
    ) -> tuple[Stakeholder, ...]:
        return await collect(
            tuple(
                _get_stakeholder(stakeholder_email=email) for email in emails
            )
        )
