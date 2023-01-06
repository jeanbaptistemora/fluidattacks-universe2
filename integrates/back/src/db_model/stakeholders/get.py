from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .types import (
    StakeholderState,
)
from .utils import (
    format_stakeholder,
    format_state,
)
from aiodataloader import (
    DataLoader,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    ErrorLoadingStakeholders,
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
from dynamodb.types import (
    Item,
)
from typing import (
    Iterable,
    Optional,
)


async def get_all_stakeholders() -> tuple[Stakeholder, ...]:
    primary_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={"all": "all"},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ALL_STAKEHOLDERS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingStakeholders()

    return tuple(format_stakeholder(item) for item in response.items)


async def _get_stakeholder_items(
    *, emails: tuple[str, ...]
) -> tuple[Item, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["stakeholder_metadata"],
            values={"email": email},
        )
        for email in emails
    )

    return await operations.batch_get_item(keys=primary_keys, table=TABLE)


async def get_historic_state(*, email: str) -> tuple[StakeholderState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_state"],
        values={
            "email": email,
        },
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["stakeholder_historic_state"],),
        table=TABLE,
    )

    return tuple(format_state(state) for state in response.items)


async def _get_stakeholders_no_fallback(
    *, emails: tuple[str, ...]
) -> tuple[Stakeholder, ...]:
    emails = tuple(email.lower().strip() for email in emails)
    items = await _get_stakeholder_items(emails=emails)

    if len(items) != len(emails):
        raise StakeholderNotFound()

    return tuple(
        next(
            format_stakeholder(item)
            for item in items
            if (item.get("email") or str(item["pk"]).split("#")[1]) == email
        )
        for email in emails
    )


async def _get_stakeholders_with_fallback(
    *,
    stakeholder_dataloader: DataLoader,
    emails: tuple[str, ...],
) -> tuple[Stakeholder, ...]:
    emails = tuple(email.lower().strip() for email in emails)
    items = await _get_stakeholder_items(emails=emails)

    stakeholders: list[Stakeholder] = []
    for email in emails:
        stakeholder: Optional[Stakeholder] = next(
            (
                format_stakeholder(item)
                for item in items
                if item.get("email") == email
            ),
            None,
        )
        if stakeholder:
            stakeholder_dataloader.prime(email, stakeholder)
        else:
            stakeholder = Stakeholder(email=email)
        stakeholders.append(stakeholder)

    return tuple(stakeholders)


class StakeholderLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[Stakeholder, ...]:
        return await _get_stakeholders_no_fallback(emails=tuple(emails))


class StakeholderWithFallbackLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[Stakeholder, ...]:
        return await _get_stakeholders_with_fallback(
            stakeholder_dataloader=self.dataloader, emails=tuple(emails)
        )
