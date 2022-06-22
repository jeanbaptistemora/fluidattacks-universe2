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
from newutils import (
    stakeholders as stakeholders_utils,
)
from stakeholders import (
    dal as stakeholders_dal,
)


async def _get_stakeholder(*, email: str) -> Stakeholder:
    item_legacy = await stakeholders_dal.get(email)
    if not item_legacy:
        raise StakeholderNotFound()

    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item_vms = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )

    return stakeholders_utils.format_stakeholder(item_legacy, item_vms)


class StakeholderTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: tuple[str, ...]
    ) -> tuple[Stakeholder, ...]:
        return await collect(
            tuple(_get_stakeholder(email=email) for email in emails)
        )
