from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputMetadataToUpdate,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)


async def add(
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
) -> None:
    toe_input = ToeInput(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=attributes.be_present_until,
        component=component,
        entry_point=entry_point,
        first_attack_at=attributes.first_attack_at,
        group_name=group_name,
        seen_at=attributes.seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        unreliable_root_id=attributes.unreliable_root_id,
    )
    await toe_inputs_model.add(toe_input=toe_input)


async def remove(entry_point: str, component: str, group_name: str) -> None:
    await toe_inputs_model.remove(
        entry_point=entry_point, component=component, group_name=group_name
    )


async def update(
    current_value: ToeInput,
    attributes: ToeInputAttributesToUpdate,
) -> None:
    metadata = ToeInputMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=attributes.be_present_until,
        first_attack_at=attributes.first_attack_at,
        seen_at=attributes.seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        unreliable_root_id=attributes.unreliable_root_id,
        clean_attacked_at=attributes.clean_attacked_at,
        clean_be_present_until=attributes.clean_be_present_until,
        clean_first_attack_at=attributes.clean_first_attack_at,
    )
    await toe_inputs_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
