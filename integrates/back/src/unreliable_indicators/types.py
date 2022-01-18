from typing import (
    Dict,
    List,
    NamedTuple,
    Set,
)
from unreliable_indicators.enums import (
    EntityAttr,
    EntityId,
)


class EntityToUpdate(NamedTuple):
    entity_ids: Dict[EntityId, List[str]]
    attributes_to_update: Set[EntityAttr]
