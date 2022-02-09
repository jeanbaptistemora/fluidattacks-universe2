from custom_exceptions import (
    InvalidToeInputAttackedAt,
    InvalidToeInputAttackedBy,
    ToeInputNotPresent,
)
from custom_types import (
    Group,
)
from datetime import (
    datetime,
)
from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.roots.types import (
    GitRootItem,
    IPRootItem,
    RootItem,
    URLRootItem,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputMetadataToUpdate,
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
    Any,
    Optional,
    Tuple,
)


def _get_optional_be_present_until(
    be_present: bool,
) -> Optional[datetime]:
    return datetime_utils.get_utc_now() if be_present is False else None


async def add(
    loaders: Any,
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
) -> None:
    formatted_component = component.strip()
    while formatted_component.endswith("/"):
        formatted_component = formatted_component[:-1].strip()

    if attributes.is_moving_toe_input is False:
        root: RootItem = await loaders.root.load(
            (group_name, attributes.unreliable_root_id)
        )
        validate_active_root(root)
        validate_component(root, formatted_component)

    be_present_until = _get_optional_be_present_until(attributes.be_present)
    first_attack_at = attributes.first_attack_at or attributes.attacked_at
    has_vulnerabilities = get_has_vulnerabilities(
        attributes.be_present, attributes.has_vulnerabilities
    )
    seen_at = (
        attributes.seen_at or first_attack_at or datetime_utils.get_utc_now()
    )
    toe_input = ToeInput(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        component=formatted_component,
        entry_point=entry_point,
        first_attack_at=first_attack_at,
        group_name=group_name,
        has_vulnerabilities=has_vulnerabilities,
        seen_at=seen_at,
        seen_first_time_by=attributes.seen_first_time_by,
        unreliable_root_id=attributes.unreliable_root_id,
    )
    await toe_inputs_model.add(toe_input=toe_input)


def _get_host(url: str) -> str:
    return url.split("/")[0].split(":")[0]


def _get_port(url: str) -> Optional[str]:
    return (
        url.split("/")[0].split(":")[1] if ":" in url.split("/")[0] else None
    )


def _get_path(url: str) -> str:
    return url.split("/", maxsplit=1)[1] if "/" in url else ""


def _get_protocol(url: str) -> str:
    if (index := url.find("://")) != -1:
        return url[:index].lower()
    return "unknown"


def _get_www(url: str) -> str:
    pattern = "www."
    if pattern in url:
        return pattern
    return ""


def _format_component(component: str) -> str:
    return (
        component.strip()
        .replace("https://", "")
        .replace("http://", "")
        .replace("unknown://", "")
        .replace("unknown//", "")
        .replace("www.", "")
    )


def _format_unreliable_component(
    root: RootItem, component: str
) -> Tuple[Optional[RootItem], str]:
    if component.endswith("/"):
        return root, component[:-1]
    return root, component


def get_reduced_component(component: str, entry_point: str) -> str:
    formatted_component = _format_component(component)
    host = _get_host(formatted_component)
    path = _get_path(formatted_component)
    return f"{host}/{path}/{entry_point}"


def get_unreliable_component(  # pylint: disable=too-many-locals
    component: str, group_roots: Tuple[RootItem, ...], group: Group
) -> Tuple[Optional[RootItem], Optional[str]]:
    if not component:
        return None, None

    has_black_service = group["service"] == "BLACK"
    has_white_service = group["service"] == "WHITE"
    formatted_component = _format_component(component)
    host = _get_host(formatted_component)
    port = _get_port(formatted_component)
    path = _get_path(formatted_component)
    protocol = _get_protocol(component.strip())
    host_and_port = f"{host}:{port}" if port else host
    for root in group_roots:
        if has_white_service and isinstance(root, GitRootItem):
            for env_url in root.state.environment_urls:
                formatted_root_url = _format_component(env_url)
                formatted_root_host = _get_host(formatted_root_url)
                formatted_root_port = _get_port(formatted_root_url)
                root_www = _get_www(env_url)
                root_host_and_port = (
                    f"{formatted_root_host}:{formatted_root_port}"
                    if formatted_root_port
                    else formatted_root_host
                )
                root_protocol = _get_protocol(env_url.strip())
                if f"{host}" == f"{formatted_root_host}":
                    return _format_unreliable_component(
                        root,
                        f"{root_protocol.lower()}://{root_www}"
                        f"{root_host_and_port}/{path}",
                    )

        if has_black_service and isinstance(root, URLRootItem):
            root_host_and_port = (
                f"{root.state.host}:{root.state.port}"
                if root.state.port
                else root.state.host
            )
            formatted_root_url = _format_component(
                (
                    f"{root.state.protocol.lower()}://{root_host_and_port}"
                    f"{root.state.path}"
                )
            )
            formatted_root_host = _get_host(formatted_root_url)
            formatted_root_path = _get_path(formatted_root_url)
            formatted_root_port = _get_port(formatted_root_url)
            if f"{host}/{path}".startswith(
                f"{formatted_root_host}/{formatted_root_path}"
            ) and (not port or port == formatted_root_port):
                return _format_unreliable_component(
                    root,
                    f"{root.state.protocol.lower()}://{root_host_and_port}/"
                    f"{path}",
                )

        if has_black_service and isinstance(root, IPRootItem):
            root_host_and_port = (
                f"{root.state.address}:{root.state.port}"
                if root.state.port
                else root.state.address
            )
            formatted_root_url = _format_component(root_host_and_port)
            formatted_root_host = _get_host(formatted_root_url)
            formatted_root_port = _get_port(formatted_root_url)
            if (
                host == formatted_root_host
                or host.startswith(f"{formatted_root_host}/")
            ) and (not port or port == formatted_root_port):
                return _format_unreliable_component(
                    root, f"{root_host_and_port}/{path}"
                )

    return _format_unreliable_component(
        None, f"{protocol}://{host_and_port}/{path}"
    )


async def remove(
    current_value: ToeInput,
) -> None:
    await toe_inputs_model.remove(
        entry_point=current_value.entry_point,
        component=current_value.component,
        group_name=current_value.group_name,
    )


async def update(
    current_value: ToeInput,
    attributes: ToeInputAttributesToUpdate,
) -> None:
    if attributes.is_moving_toe_input is False:
        if (
            attributes.be_present is None
            and current_value.be_present is False
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
            and current_value.attacked_at is not None
            and attributes.attacked_at <= current_value.attacked_at
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and attributes.attacked_at > datetime_utils.get_utc_now()
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and current_value.seen_at is not None
            and attributes.attacked_at < current_value.seen_at
        ):
            raise InvalidToeInputAttackedAt()
        if (
            attributes.attacked_at is not None
            and attributes.attacked_by is None
        ):
            raise InvalidToeInputAttackedBy()

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

    metadata = ToeInputMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        first_attack_at=first_attack_at,
        has_vulnerabilities=has_vulnerabilities,
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
