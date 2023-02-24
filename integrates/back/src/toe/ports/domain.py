from custom_exceptions import (
    InvalidIpAddressInRoot,
    InvalidPort,
    InvalidRootType,
    InvalidToePortAttackedAt,
    InvalidToePortAttackedBy,
    ToePortNotPresent,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    toe_ports as toe_ports_model,
)
from db_model.roots.types import (
    IPRoot,
)
from db_model.toe_ports.types import (
    ToePort,
    ToePortState,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_fields_deco,
)
from roots import (
    domain as roots_domain,
)
from roots.validations import (
    validate_active_root,
)
from toe.ports.types import (
    ToePortAttributesToAdd,
    ToePortAttributesToUpdate,
)
from toe.utils import (
    get_has_vulnerabilities,
)


def _get_optional_be_present_until(be_present: bool) -> datetime | None:
    return datetime_utils.get_utc_now() if be_present is False else None


@validate_fields_deco(["address"])
async def add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    address: str,
    port: str,
    root_id: str,
    attributes: ToePortAttributesToAdd,
    modified_by: str,
    is_moving_toe_port: bool = False,
) -> None:
    root = await roots_domain.get_root(loaders, root_id, group_name)
    if not isinstance(root, IPRoot):
        raise InvalidRootType()
    if is_moving_toe_port is False:
        validate_active_root(root)
        if root.state.address != address:
            raise InvalidIpAddressInRoot()
        if not 0 <= int(port) <= 65535:
            raise InvalidPort(expr=f'"values": "{port}"')

    be_present_until = _get_optional_be_present_until(attributes.be_present)
    first_attack_at = attributes.first_attack_at or attributes.attacked_at
    has_vulnerabilities = get_has_vulnerabilities(
        attributes.be_present, attributes.has_vulnerabilities
    )
    seen_at = (
        attributes.seen_at or first_attack_at or datetime_utils.get_utc_now()
    )
    toe_port = ToePort(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        seen_at=seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        state=ToePortState(
            attacked_at=attributes.attacked_at,
            attacked_by=attributes.attacked_by,
            be_present=attributes.be_present,
            be_present_until=be_present_until,
            first_attack_at=first_attack_at,
            has_vulnerabilities=has_vulnerabilities,
            modified_date=datetime_utils.get_utc_now(),
            modified_by=modified_by,
        ),
    )
    await toe_ports_model.add(toe_port=toe_port)


async def remove(
    current_value: ToePort,
) -> None:
    await toe_ports_model.remove(
        port=current_value.port,
        address=current_value.address,
        group_name=current_value.group_name,
        root_id=current_value.root_id,
    )


def _validate_update(
    current_value: ToePort,
    attributes: ToePortAttributesToUpdate,
) -> None:
    if (
        attributes.be_present is None
        and current_value.state.be_present is False
        and attributes.attacked_at is not None
    ):
        raise ToePortNotPresent()
    if attributes.be_present is False and attributes.attacked_at is not None:
        raise ToePortNotPresent()
    if (
        attributes.attacked_at is not None
        and current_value.state.attacked_at is not None
        and attributes.attacked_at <= current_value.state.attacked_at
    ):
        raise InvalidToePortAttackedAt()
    if (
        attributes.attacked_at is not None
        and attributes.attacked_at > datetime_utils.get_utc_now()
    ):
        raise InvalidToePortAttackedAt()
    if (
        attributes.attacked_at is not None
        and current_value.seen_at is not None
        and attributes.attacked_at < current_value.seen_at
    ):
        raise InvalidToePortAttackedAt()
    if attributes.attacked_at is not None and attributes.attacked_by is None:
        raise InvalidToePortAttackedBy()


async def update(
    current_value: ToePort,
    attributes: ToePortAttributesToUpdate,
    modified_by: str,
    is_moving_toe_port: bool = False,
) -> None:
    if is_moving_toe_port is False:
        _validate_update(current_value, attributes)

    updated_attacked_at = (
        current_value.state.attacked_at
        if attributes.attacked_at is None
        else attributes.attacked_at
    )
    updated_attacked_by = (
        current_value.state.attacked_by
        if attributes.attacked_by is None
        else attributes.attacked_by
    )
    updated_be_present = (
        current_value.state.be_present
        if attributes.be_present is None
        else attributes.be_present
    )
    updated_be_present_until = (
        current_value.state.be_present_until
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    updated_first_attack_at = current_value.state.first_attack_at
    if attributes.first_attack_at is not None:
        updated_first_attack_at = attributes.first_attack_at
    elif not current_value.state.first_attack_at and attributes.attacked_at:
        updated_first_attack_at = attributes.attacked_at
    updated_has_vulnerabilities = (
        get_has_vulnerabilities(
            updated_be_present, attributes.has_vulnerabilities
        )
        if attributes.has_vulnerabilities is not None
        or attributes.be_present is not None
        else current_value.state.has_vulnerabilities
    )

    if not (
        updated_attacked_at == current_value.state.attacked_at
        and updated_attacked_by == current_value.state.attacked_by
        and updated_be_present == current_value.state.be_present
        and updated_be_present_until == current_value.state.be_present_until
        and updated_has_vulnerabilities
        == current_value.state.has_vulnerabilities
    ):
        await toe_ports_model.update_state(
            current_value=current_value,
            state=ToePortState(
                attacked_at=updated_attacked_at,
                attacked_by=updated_attacked_by,
                be_present=updated_be_present,
                be_present_until=updated_be_present_until,
                first_attack_at=updated_first_attack_at,
                has_vulnerabilities=updated_has_vulnerabilities,
                modified_date=datetime_utils.get_utc_now(),
                modified_by=modified_by,
            ),
        )
