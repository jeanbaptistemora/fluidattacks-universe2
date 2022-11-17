# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    InvalidRootType,
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
)
from newutils import (
    datetime as datetime_utils,
)
from roots.validations import (
    validate_active_root,
    validate_ip_and_port_in_root,
)
from toe.ports.types import (
    ToePortAttributesToAdd,
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


async def add(  # pylint: disable=too-many-arguments,invalid-name
    loaders: Dataloaders,
    group_name: str,
    ip: str,
    port: str,
    root_id: str,
    attributes: ToePortAttributesToAdd,
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    if not isinstance(root, IPRoot):
        raise InvalidRootType()
    validate_active_root(root)
    validate_ip_and_port_in_root(root, ip, port)

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
        ip=ip,
        port=port,
        first_attack_at=first_attack_at,
        group_name=group_name,
        has_vulnerabilities=has_vulnerabilities,
        seen_at=seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        root_id=root_id,
    )
    await toe_ports_model.add(toe_port=toe_port)


async def remove(
    current_value: ToePort,
) -> None:
    await toe_ports_model.remove(
        port=current_value.port,
        ip=current_value.ip,
        group_name=current_value.group_name,
        root_id=current_value.root_id,
    )
