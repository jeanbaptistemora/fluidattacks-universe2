import pytest
from unreliable_indicators import (
    model,
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
pytestmark = [
    pytest.mark.asyncio,
]


def test_model_entity_names_integrity() -> None:
    entity_names = list(key.value for key in model.ENTITIES)
    assert entity_names == sorted(entity_names)


def test_model_entity_attrs_integrity() -> None:
    for entity in model.ENTITIES.values():
        entity_attrs = entity["attrs"]
        assert isinstance(entity_attrs, dict)
        entity_attrs_keys = [str(ent) for ent in entity_attrs.keys()]
        assert entity_attrs_keys == sorted(entity_attrs_keys)


def test_get_entities_to_update_by_dependency() -> None:
    finding_id = "422286126"
    vulnerability_id = "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    entities_to_update_by_dependency = (
        model.get_entities_to_update_by_dependency(
            EntityDependency.request_vulnerabilities_zero_risk,
            finding_ids=[finding_id],
            vulnerability_ids=[vulnerability_id],
        )
    )
    expected_output = {
        Entity.vulnerability: EntityToUpdate(
            entity_ids={EntityId.ids: [vulnerability_id]},
            attributes_to_update={
                EntityAttr.last_reattack_date,
                EntityAttr.treatment_changes,
            },
        ),
        Entity.finding: EntityToUpdate(
            entity_ids={EntityId.ids: [finding_id]},
            attributes_to_update={
                EntityAttr.newest_vulnerability_report_date,
                EntityAttr.oldest_vulnerability_report_date,
                EntityAttr.oldest_open_vulnerability_report_date,
                EntityAttr.open_vulnerabilities,
                EntityAttr.status,
                EntityAttr.treatment_summary,
                EntityAttr.verification_summary,
                EntityAttr.where,
            },
        ),
    }
    assert entities_to_update_by_dependency == expected_output
