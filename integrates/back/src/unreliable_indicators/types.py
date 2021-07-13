from typing import (
    Dict,
    NamedTuple,
    Set,
)
from unreliable_indicators.enums import (
    EntityAttrName,
    EntityIdName,
)


class EntityToUpdate(NamedTuple):
    entity_ids: Dict[EntityIdName, str]
    attributes_to_update: Set[EntityAttrName]
