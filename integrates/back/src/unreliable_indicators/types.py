# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
