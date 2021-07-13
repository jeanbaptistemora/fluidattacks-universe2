from typing import (
    cast,
    Dict,
)
from unreliable_indicators.enums import (
    EntityAttrName,
    EntityIdName,
    EntityName,
)
from unreliable_indicators.types import (
    EntityToUpdate,
)

# Constants
ENTITIES = {
    EntityName.finding: dict(
        args={
            EntityIdName.id,
            EntityIdName.group,
        },
        attrs={
            EntityAttrName.unreliable_age: dict(dependencies=set()),
            EntityAttrName.unreliable_closed_vulnerabilities: dict(
                dependencies=set()
            ),
            EntityAttrName.unreliable_is_verified: dict(dependencies=set()),
            EntityAttrName.unreliable_last_vulnerability: dict(
                dependencies=set()
            ),
            EntityAttrName.unreliable_open_age: dict(dependencies=set()),
            EntityAttrName.unreliable_open_vulnerabilities: dict(
                dependencies=set()
            ),
            EntityAttrName.unreliable_report_date: dict(dependencies=set()),
            EntityAttrName.unreliable_status: dict(dependencies=set()),
        },
    ),
}


def get_entities_to_update_by_dependency(
    dependency: str, **args: str
) -> Dict[EntityName, EntityToUpdate]:
    entities_to_update = dict()
    for entity_name in ENTITIES:
        attributes_to_update = set()
        for attr, info in cast(dict, ENTITIES[entity_name]["attrs"]).items():
            if dependency in info["dependencies"]:
                attributes_to_update.add(attr)

        if attributes_to_update:
            entity_args = cast(set, ENTITIES[entity_name]["args"])
            entity_ids = {
                base_arg: args[f"{entity_name.value}_{base_arg.value}"]
                for base_arg in entity_args
            }
            entities_to_update[entity_name] = EntityToUpdate(
                entity_ids=entity_ids,
                attributes_to_update=attributes_to_update,
            )

    return entities_to_update
