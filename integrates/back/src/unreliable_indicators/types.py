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
    # pylint: disable=too-few-public-methods, inherit-non-class
    entity_ids: Dict[EntityId, str]
    attributes_to_update: Set[EntityAttr]
