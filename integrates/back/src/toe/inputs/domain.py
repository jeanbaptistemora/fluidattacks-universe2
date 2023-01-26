from custom_exceptions import (
    InvalidRootType,
    InvalidToeInputAttackedAt,
    InvalidToeInputAttackedBy,
    ToeInputNotPresent,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.roots.types import (
    GitRoot,
    Root,
    RootRequest,
    URLRoot,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputMetadataToUpdate,
    ToeInputState,
)
from newutils import (
    datetime as datetime_utils,
)
from roots.validations import (
    validate_active_root,
    validate_component,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)
from toe.utils import (
    get_has_vulnerabilities,
)
from typing import (
    Optional,
)


def _get_optional_be_present_until(
    be_present: bool,
) -> Optional[datetime]:
    return datetime_utils.get_utc_now() if be_present is False else None


async def add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
    is_moving_toe_input: bool = False,
) -> None:
    formatted_component = component.strip()
    if is_moving_toe_input is False:
        root: Root = await loaders.root.load(
            RootRequest(group_name, attributes.unreliable_root_id)
        )
        if not isinstance(root, (GitRoot, URLRoot)):
            raise InvalidRootType()
        validate_active_root(root)
        await validate_component(loaders, root, formatted_component)

    be_present_until = _get_optional_be_present_until(attributes.be_present)
    first_attack_at = attributes.first_attack_at or attributes.attacked_at
    has_vulnerabilities = get_has_vulnerabilities(
        attributes.be_present, attributes.has_vulnerabilities
    )
    seen_at = (
        attributes.seen_at or first_attack_at or datetime_utils.get_utc_now()
    )
    toe_input = ToeInput(
        component=formatted_component,
        entry_point=entry_point,
        group_name=group_name,
        state=ToeInputState(
            attacked_at=attributes.attacked_at,
            attacked_by=attributes.attacked_by,
            be_present=attributes.be_present,
            be_present_until=be_present_until,
            first_attack_at=first_attack_at,
            has_vulnerabilities=has_vulnerabilities,
            modified_by=attributes.seen_first_time_by,
            modified_date=datetime_utils.get_utc_now(),
            seen_at=seen_at,
            seen_first_time_by=attributes.seen_first_time_by,
            unreliable_root_id=attributes.unreliable_root_id,
        ),
    )
    await toe_inputs_model.add(toe_input=toe_input)


def _get_host(url: str) -> str:
    return url.split("/")[0].split(":")[0]


def _get_path(url: str) -> str:
    return url.split("/", maxsplit=1)[1] if "/" in url else ""


def _format_component(component: str) -> str:
    return (
        component.strip()
        .replace("https://", "")
        .replace("http://", "")
        .replace("unknown://", "")
        .replace("unknown//", "")
        .replace("www.", "")
    )


def get_reduced_component(component: str, entry_point: str) -> str:
    formatted_component = _format_component(component)
    host = _get_host(formatted_component)
    path = _get_path(formatted_component)
    return f"{host}/{path}/{entry_point}"


async def remove(
    current_value: ToeInput,
) -> None:
    await toe_inputs_model.remove(
        entry_point=current_value.entry_point,
        component=current_value.component,
        group_name=current_value.group_name,
        root_id=current_value.state.unreliable_root_id,
    )


async def update(
    current_value: ToeInput,
    attributes: ToeInputAttributesToUpdate,
    modified_by: str,
    is_moving_toe_input: bool = False,
) -> None:
    if is_moving_toe_input is False:
        if (
            attributes.be_present is None
            and current_value.state.be_present is False
            and attributes.attacked_at is not None
        ):
            raise ToeInputNotPresent()
        if (
            attributes.be_present is False
            and attributes.attacked_at is not None
        ):
            raise ToeInputNotPresent()
        if (
            attributes.attacked_at is not None
            and current_value.state.attacked_at is not None
            and attributes.attacked_at <= current_value.state.attacked_at
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and attributes.attacked_at > datetime_utils.get_utc_now()
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and current_value.state.seen_at is not None
            and attributes.attacked_at < current_value.state.seen_at
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and attributes.attacked_by is None
        ):
            raise InvalidToeInputAttackedBy()

    be_present_until = (
        current_value.state.be_present_until
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    current_be_present = (
        current_value.state.be_present
        if attributes.be_present is None
        else attributes.be_present
    )
    first_attack_at = current_value.state.first_attack_at
    if attributes.first_attack_at is not None:
        first_attack_at = attributes.first_attack_at
    elif (
        current_value.state.first_attack_at is None and attributes.attacked_at
    ):
        first_attack_at = attributes.attacked_at
    has_vulnerabilities = (
        get_has_vulnerabilities(
            current_be_present, attributes.has_vulnerabilities
        )
        if attributes.has_vulnerabilities is not None
        or attributes.be_present is not None
        else None
    )

    new_state = ToeInputState(
        attacked_at=attributes.attacked_at
        if attributes.attacked_at is not None
        else current_value.state.attacked_at,
        attacked_by=attributes.attacked_by
        if attributes.attacked_by is not None
        else current_value.state.attacked_by,
        be_present=current_be_present,
        be_present_until=be_present_until,
        first_attack_at=first_attack_at
        if first_attack_at is not None
        else current_value.state.first_attack_at,
        has_vulnerabilities=has_vulnerabilities
        if has_vulnerabilities is not None
        else current_value.state.has_vulnerabilities,
        modified_by=modified_by,
        modified_date=datetime_utils.get_utc_now(),
        seen_at=attributes.seen_at
        if attributes.seen_at is not None
        else current_value.state.seen_at,
        seen_first_time_by=attributes.seen_first_time_by
        if attributes.seen_first_time_by is not None
        else current_value.state.seen_first_time_by,
        unreliable_root_id=attributes.unreliable_root_id
        if attributes.unreliable_root_id is not None
        else current_value.state.unreliable_root_id,
    )
    metadata = ToeInputMetadataToUpdate(
        clean_attacked_at=attributes.clean_attacked_at,
        clean_be_present_until=attributes.be_present is not None
        and be_present_until is None,
        clean_first_attack_at=attributes.clean_first_attack_at,
        clean_seen_at=attributes.clean_seen_at,
    )

    await toe_inputs_model.update_state(
        current_value=current_value,
        new_state=new_state,
        metadata=metadata,
    )
