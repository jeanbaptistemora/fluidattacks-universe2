from typing import (
    cast,
    Dict,
    List,
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
            EntityId.ids,
        },
        attrs={
            EntityAttr.closed_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.is_verified: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.newest_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.oldest_open_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.oldest_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.open_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.status: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.treatment_summary: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.handle_vulnerabilities_acceptance,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.reset_expired_accepted_findings,
                    EntityDependency.update_vulnerabilities_treatment,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.where: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.update_vulnerability_commit,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
        },
    ),
    Entity.vulnerability: dict(
        args={
            EntityId.ids,
        },
        attrs={
            EntityAttr.efficacy: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.last_reattack_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.last_reattack_requester: dict(
                dependencies={
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.verify_vulnerabilities_request,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.last_requested_reattack_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.reattack_cycles: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.treatment_changes: dict(
                dependencies={
                    EntityDependency.approve_draft,
                    EntityDependency.handle_vulnerabilities_acceptance,
                    EntityDependency.handle_finding_policy,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.reset_expired_accepted_findings,
                    EntityDependency.upload_file,
                    EntityDependency.update_vulnerabilities_treatment,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
        },
    ),
}


def get_entities_to_update_by_dependency(
    dependency: EntityDependency, **args: List[str]
) -> Dict[Entity, EntityToUpdate]:
    entities_to_update = {}
    for name, value in ENTITIES.items():
        attributes_to_update = set()
        for attr, info in cast(dict, value["attrs"]).items():
            if dependency in info["dependencies"]:
                attributes_to_update.add(attr)

        if attributes_to_update:
            entity_args = cast(set, value["args"])
            entity_ids = {
                base_arg: args[f"{name.value}_{base_arg.value}"]
                for base_arg in entity_args
            }
            entities_to_update[name] = EntityToUpdate(
                entity_ids=entity_ids,
                attributes_to_update=attributes_to_update,
            )

    return entities_to_update
