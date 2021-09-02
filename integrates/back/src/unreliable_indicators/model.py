from typing import (
    cast,
    Dict,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)
from unreliable_indicators.types import (
    EntityToUpdate,
)

# Constants
ENTITIES = {
    Entity.finding: dict(
        args={
            EntityId.id,
        },
        attrs={
            EntityAttr.age: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.closed_vulnerabilities: dict(
                dependencies={
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.is_verified: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.last_vulnerability: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.open_age: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.open_vulnerabilities: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.report_date: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.status: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.where: dict(
                dependencies={
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.update_vulnerability_commit,
                    EntityDependency.upload_file,
                }
            ),
        },
    ),
}


def get_entities_to_update_by_dependency(
    dependency: EntityDependency, **args: str
) -> Dict[Entity, EntityToUpdate]:
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
