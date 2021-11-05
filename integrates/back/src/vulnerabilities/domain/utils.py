import authz
from custom_exceptions import (
    AcceptanceNotRequested,
    InvalidTreatmentManager,
)
from custom_types import (
    Finding,
    Historic,
)
from db_model.roots.types import (
    GitRootItem,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import html
from typing import (
    Any,
    cast,
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


def get_hash_from_dict(vuln: Dict[str, Any], from_yaml: bool = False) -> int:
    nonce: str = uuid().hex

    specific = vuln.get("specific", nonce)
    type_ = vuln.get("vuln_type", nonce)
    where = vuln.get("where", nonce)

    if from_yaml:
        # https://gitlab.com/fluidattacks/product/-/issues/5556#note_725588290
        specific = html.escape(specific, quote=False)
        where = html.escape(where, quote=False)

    return get_hash(specific=specific, type_=type_, where=where)


def get_hash_from_typed(vuln: Vulnerability) -> int:
    return get_hash(
        specific=vuln.specific,
        type_=vuln.type.value,
        where=vuln.where,
    )


def compare_historic_treatments(
    last_state: Dict[str, str], new_state: Dict[str, str]
) -> bool:
    excluded_attrs = {"acceptance_date", "acceptance_status", "date", "user"}
    last_values = [
        value for key, value in last_state.items() if key not in excluded_attrs
    ]
    new_values = [
        value for key, value in new_state.items() if key not in excluded_attrs
    ]
    date_change = (
        "acceptance_date" in new_state
        and "acceptance_date" in last_state
        and last_state["acceptance_date"].split(" ")[0]
        != new_state["acceptance_date"].split(" ")[0]
    )
    return (sorted(last_values) != sorted(new_values)) or date_change


def validate_acceptance(vuln: Dict[str, Finding]) -> Dict[str, Finding]:
    historic_treatment = cast(Historic, vuln.get("historic_treatment", [{}]))
    if historic_treatment[-1].get("acceptance_status") != "SUBMITTED":
        raise AcceptanceNotRequested()
    return vuln


async def validate_treatment_manager(
    *,
    treatment_manager: str,
    is_customer_admin: bool,
    user_email: str,
    group_name: str,
) -> str:
    if not is_customer_admin:
        treatment_manager = user_email
    enforcer = await authz.get_group_level_enforcer(treatment_manager)
    if not enforcer(group_name, "valid_treatment_manager"):
        raise InvalidTreatmentManager()
    return treatment_manager


async def get_root_nicknames_for_skims(
    dataloaders: Any,
    group: str,
    vulnerabilities: List[Dict[str, Any]],
) -> Set[str]:
    # If a vuln is linked to a root, return it
    # otherwise return all roots, the vuln must belong to one of them
    include_all: bool = False
    root_nicknames: Set[str] = set()

    for vuln in vulnerabilities:
        if vuln.get("repo_nickname"):  # Exists and truthy
            root_nicknames.add(vuln["repo_nickname"])
        else:
            include_all = True

    if include_all:
        root_nicknames.update(
            root.state.nickname
            for root in await dataloaders.group_roots.load(group)
            if isinstance(root, GitRootItem)
        )

    return root_nicknames
