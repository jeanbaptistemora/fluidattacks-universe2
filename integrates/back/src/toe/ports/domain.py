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
    Root,
)
from db_model.toe_ports.types import (
    ToePort,
    ToePortMetadataToUpdate,
    ToePortState,
)
from newutils import (
    datetime as datetime_utils,
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
    address: str,
    port: str,
    root_id: str,
    attributes: ToePortAttributesToAdd,
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    if not isinstance(root, IPRoot):
        raise InvalidRootType()
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
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        address=address,
        port=port,
        first_attack_at=first_attack_at,
        group_name=group_name,
        has_vulnerabilities=has_vulnerabilities,
        seen_at=seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        state=ToePortState(modified_date=datetime_utils.get_utc_now()),
        root_id=root_id,
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
        and current_value.be_present is False
        and attributes.attacked_at is not None
    ):
        raise ToePortNotPresent()
    if attributes.be_present is False and attributes.attacked_at is not None:
        raise ToePortNotPresent()
    if (
        attributes.attacked_at is not None
        and current_value.attacked_at is not None
        and attributes.attacked_at <= current_value.attacked_at
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
    is_moving_toe_port: bool = False,
) -> None:
    if is_moving_toe_port is False:
        _validate_update(current_value, attributes)

    be_present_until = (
        None
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    current_be_present = (
        current_value.be_present
        if attributes.be_present is None
        else attributes.be_present
    )
    first_attack_at = None
    if attributes.first_attack_at is not None:
        first_attack_at = attributes.first_attack_at
    elif not current_value.first_attack_at and attributes.attacked_at:
        first_attack_at = attributes.attacked_at
    has_vulnerabilities = (
        get_has_vulnerabilities(
            current_be_present, attributes.has_vulnerabilities
        )
        if attributes.has_vulnerabilities is not None
        or attributes.be_present is not None
        else None
    )

    metadata = ToePortMetadataToUpdate(
        state=ToePortState(modified_date=datetime_utils.get_utc_now()),
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        first_attack_at=first_attack_at,
        has_vulnerabilities=has_vulnerabilities,
        seen_at=attributes.seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        clean_attacked_at=attributes.clean_attacked_at,
        clean_be_present_until=attributes.be_present is not None
        and be_present_until is None,
        clean_first_attack_at=attributes.clean_first_attack_at,
        clean_seen_at=attributes.clean_seen_at,
    )
    await toe_ports_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
