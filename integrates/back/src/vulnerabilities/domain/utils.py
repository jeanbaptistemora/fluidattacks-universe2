import authz
from custom_exceptions import (
    AcceptanceNotRequested,
    InvalidAssigned,
    StakeholderNotFound,
)
from datetime import (
    datetime,
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
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
import html
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Dict,
    List,
    Set,
)
from uuid import (
    uuid4 as uuid,
)


def get_hash(specific: str, type_: str, where: str) -> int:
    # Return a unique identifier according to the business rules
    return hash((specific, type_, where))


def get_hash_from_dict(vuln: Dict[str, Any]) -> int:
    nonce: str = uuid().hex
    specific = vuln.get("specific", nonce)
    type_ = vuln.get("vuln_type", nonce)
    where = vuln.get("where", nonce)
    return get_hash(specific=specific, type_=type_, where=where)


def get_hash_from_typed(vuln: Vulnerability, from_yaml: bool = False) -> int:
    specific = vuln.specific
    type_ = vuln.type.value
    where = vuln.where
    if from_yaml:
        # https://gitlab.com/fluidattacks/product/-/issues/5556#note_725588290
        specific = html.escape(specific, quote=False)
        where = html.escape(where, quote=False)
    return get_hash(specific=specific, type_=type_, where=where)


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
        and datetime.fromisoformat(last_state.accepted_until)
        != datetime_utils.get_from_str(new_state["acceptance_date"])
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
    loaders: Any,
    assigned: str,
    is_manager: bool,
    user_email: str,
    group_name: str,
) -> str:
    if not is_manager:
        assigned = user_email
    enforcer = await authz.get_group_level_enforcer(assigned)
    try:
        stakeholder: Stakeholder = await loaders.stakeholder.load(assigned)
    except StakeholderNotFound:
        stakeholder = Stakeholder(
            email=assigned, first_name="", last_name="", is_registered=False
        )
    if (
        not enforcer(group_name, "valid_assigned")
        or not stakeholder.is_registered
    ):
        raise InvalidAssigned()
    return assigned


async def get_root_nicknames_for_skims(
    dataloaders: Any,
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
        roots: tuple[Root, ...] = await dataloaders.group_roots.load(group)
        root_nicknames.update(
            root.state.nickname
            for root in roots
            if root.id in non_duplicate_root_ids
        )
    else:
        root_nicknames.update(
            root.state.nickname
            for root in await dataloaders.group_roots.load(group)
            if isinstance(root, GitRoot)
        )

    return root_nicknames


def format_vulnerability_locations(where: List[str]) -> str:
    location_str: str = ""
    for location in where:
        location_str += f"- {location}\n"
    return location_str
