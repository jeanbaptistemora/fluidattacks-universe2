from typing import (
    Any,
    NamedTuple,
)
from unreliable_indicators.enums import (
    EntityAttr,
    EntityId,
)


class EntityToUpdate(NamedTuple):
    entity_ids: dict[EntityId, list[Any]]
    attributes_to_update: set[EntityAttr]
