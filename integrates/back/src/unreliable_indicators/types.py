from typing import (
    Dict,
    NamedTuple,
    Set,
)
from unreliable_indicators.enums import (
    EntityAttr,
    EntityId,
)


class EntityToUpdate(NamedTuple):
    entity_ids: Dict[EntityId, str]
    attributes_to_update: Set[EntityAttr]
