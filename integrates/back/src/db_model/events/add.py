from .types import (
    Event,
)
from custom_exceptions import (
    EventAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.events.constants import (
    GSI_2_FACET,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.utils import (
    format_event_item,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json


async def add(*, event: Event) -> None:
    items = []
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event.id,
            "name": event.group_name,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "is_solved": str(
                event.state.status is EventStateStatus.SOLVED
            ).lower(),
            "group_name": event.group_name,
        },
    )

    item_in_db = await operations.get_item(
        facets=(TABLE.facets["event_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if item_in_db:
        raise EventAlreadyCreated.new()

    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        **format_event_item(event),
    }
    items.append(item)

    state_key = keys.build_key(
        facet=TABLE.facets["event_historic_state"],
        values={
            "id": event.id,
            "iso8601utc": event.state.modified_date,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(event.state)),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
