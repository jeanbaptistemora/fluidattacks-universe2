import authz
from custom_exceptions import (
    AcceptanceNotRequested,
    InvalidAssigned,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
import html
from newutils.vulnerabilities import (
    ignore_advisories,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)
from uuid import (
    uuid4 as uuid,
)


def get_hash(
    specific: str, type_: str, where: str, root_id: Optional[str] = None
) -> int:
    # Return a unique identifier according to the business rules
    items: Tuple[str, ...] = (specific, type_, where)
    if root_id:
        items = (*items, root_id)
    return hash(items)


def get_hash_from_dict(vuln: Dict[str, Any]) -> int:
    nonce: str = uuid().hex
    specific = vuln.get("specific", nonce)
    type_ = vuln.get("vuln_type", nonce)
    where = vuln.get("where", nonce)
    return get_hash(specific=specific, type_=type_, where=where)


def get_path_from_integrates_vulnerability(
    vulnerability_where: str,
    vulnerability_type: VulnerabilityType,
    ignore_cve: bool = False,
) -> Tuple[str, str]:
    if vulnerability_type in {
        VulnerabilityType.INPUTS,
        VulnerabilityType.PORTS,
    }:
        if len(chunks := vulnerability_where.rsplit(" (", maxsplit=1)) == 2:
            where, namespace = chunks
            namespace = namespace[:-1]
        else:
            where, namespace = chunks[0], ""
    else:
        where = vulnerability_where
        namespace = ""
    if ignore_cve:
        where = ignore_advisories(where)
    return namespace, where


def get_hash_from_typed(
    vuln: Vulnerability,
    from_yaml: bool = False,
    validate_root: bool = True,
    ignore_cve: bool = False,
) -> int:
    specific = vuln.state.specific
    type_ = vuln.type.value
    where = vuln.state.where
    if validate_root:
        where = (
            get_path_from_integrates_vulnerability(
                vuln.state.where, vuln.type
            )[1]
            if vuln.type == VulnerabilityType.INPUTS
            else vuln.state.where
        )
    if from_yaml:
        # https://gitlab.com/fluidattacks/universe/-/issues/5556#note_725588290
        specific = html.escape(specific, quote=False)
        where = html.escape(where, quote=False)
    if ignore_cve:
        where = ignore_advisories(where)
    return get_hash(
        specific=specific,
        type_=type_,
        where=where,
        root_id=(vuln.root_id if validate_root else None),
    )


def compare_historic_treatments(
    last_state: VulnerabilityTreatment, new_state: Dict[str, str]
) -> bool:
    treatment_changed = (
        last_state.status
        != VulnerabilityTreatmentStatus(
            new_state["treatment"].replace(" ", "_").upper()
        )
        or last_state.justification != new_state["justification"]
        or last_state.assigned != new_state.get("assigned")
    )
    date_changed = (
        "acceptance_date" in new_state
        and bool(new_state.get("acceptance_date"))
        and last_state.accepted_until
        and last_state.accepted_until
        != datetime.fromisoformat(new_state["acceptance_date"]).astimezone(
            tz=timezone.utc
        )
    )
    return treatment_changed or bool(date_changed)


def validate_acceptance(vuln: Vulnerability) -> None:
    if (
        vuln.treatment
        and vuln.treatment.acceptance_status
        != VulnerabilityAcceptanceStatus.SUBMITTED
    ):
        raise AcceptanceNotRequested()


async def get_valid_assigned(
    *,
    loaders: Dataloaders,
    assigned: str,
    is_manager: bool,
    email: str,
    group_name: str,
) -> str:
    if not is_manager:
        assigned = email
    group_enforcer = await authz.get_group_level_enforcer(loaders, assigned)
    stakeholder: Stakeholder = await loaders.stakeholder_with_fallback.load(
        assigned
    )
    if (
        not group_enforcer(group_name, "valid_assigned")
        or not stakeholder.is_registered
    ):
        raise InvalidAssigned()
    user_enforcer = await authz.get_user_level_enforcer(loaders, email)
    if assigned.endswith(authz.FLUID_IDENTIFIER) and not user_enforcer(
        "can_assign_vulnerabilities_to_fluidattacks_staff"
    ):
        raise InvalidAssigned()

    return assigned


async def get_root_nicknames_for_skims(
    loaders: Dataloaders,
    group: str,
    vulnerabilities: tuple[Vulnerability, ...],
) -> Set[str]:
    # If a vuln is linked to a root, return it
    # otherwise return all roots, the vuln must belong to one of them
    root_nicknames: Set[str] = set()

    root_ids: tuple[str, ...] = tuple(
        vulnerability.root_id
        for vulnerability in vulnerabilities
        if vulnerability.root_id
    )
    if len(vulnerabilities) == len(root_ids):
        non_duplicate_root_ids: set[str] = set(root_ids)
        roots: tuple[Root, ...] = await loaders.group_roots.load(group)
        root_nicknames.update(
            root.state.nickname
            for root in roots
            if root.id in non_duplicate_root_ids
        )
    else:
        root_nicknames.update(
            root.state.nickname
            for root in await loaders.group_roots.load(group)
            if isinstance(root, GitRoot)
        )

    return root_nicknames


def format_vulnerability_locations(where: List[str]) -> str:
    location_str: str = ""
    for location in set(where):
        location_str += f"{location}\n"
    return location_str
