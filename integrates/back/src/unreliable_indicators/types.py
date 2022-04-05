from typing import (
    Any,
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
    entity_ids: Dict[EntityId, List[Any]]
    attributes_to_update: Set[EntityAttr]
