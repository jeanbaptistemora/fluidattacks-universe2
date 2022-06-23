from .utils import (
    format_stakeholder,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_stakeholder(*, email: str) -> Stakeholder:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        raise StakeholderNotFound()

    return format_stakeholder(item)


class StakeholderTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: tuple[str, ...]
    ) -> tuple[Stakeholder, ...]:
        return await collect(
            tuple(_get_stakeholder(email=email) for email in emails)
        )
