from datetime import (
    datetime,
)
from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputMetadataToUpdate,
)
from newutils import (
    datetime as datetime_utils,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)
from typing import (
    Optional,
)


def _get_optional_be_present_until(
    be_present: bool,
) -> Optional[datetime]:
    return datetime_utils.get_utc_now() if be_present is False else None


async def add(
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
) -> None:
    be_present_until = _get_optional_be_present_until(attributes.be_present)
    toe_input = ToeInput(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        component=component,
        entry_point=entry_point,
        first_attack_at=attributes.first_attack_at,
        group_name=group_name,
        has_vulnerabilities=attributes.has_vulnerabilities,
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
    be_present_until = (
        None
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    metadata = ToeInputMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        first_attack_at=attributes.first_attack_at,
        has_vulnerabilities=attributes.has_vulnerabilities,
        seen_at=attributes.seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        unreliable_root_id=attributes.unreliable_root_id,
        clean_attacked_at=attributes.clean_attacked_at,
        clean_be_present_until=attributes.be_present is not None
        and be_present_until is None,
        clean_first_attack_at=attributes.clean_first_attack_at,
        clean_seen_at=attributes.clean_seen_at,
    )
    await toe_inputs_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
