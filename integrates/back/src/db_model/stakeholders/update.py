from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .types import (
    StakeholderMetadataToUpdate,
    StakeholderState,
)
from .utils import (
    format_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
)
from db_model import (
    TABLE,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


async def update_metadata(
    *,
    email: str,
    metadata: StakeholderMetadataToUpdate,
) -> None:
    email = email.lower().strip()
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": email,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={
            "all": "all",
            "email": email,
        },
    )
    item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        "email": email,
        **format_metadata_item(metadata),
    }
    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def update_state(
    *,
    user_email: str,
    state: StakeholderState,
) -> None:
    if state.modified_date is None:
        raise InvalidParameter("modified_date")

    email = user_email.lower().strip()
    key_structure = TABLE.primary_key
    state_item: Item = json.loads(
        json.dumps(state, default=serialize), parse_float=Decimal
    )
    state_item = {
        key: None if not value and value is not False else value
        for key, value in state_item.items()
        if value is not None
    }

    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": email,
        },
    )
    item = {"state": state_item}
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=item,
        key=primary_key,
        table=TABLE,
    )

    historic_state_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_state"],
        values={
            "email": email,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["stakeholder_historic_state"],
        item=historic_item,
        table=TABLE,
    )
