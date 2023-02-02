import authz
from custom_exceptions import (
    AcceptanceNotRequested,
    FindingNotFound,
    InvalidAssigned,
    InvalidParameter,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import hashlib
import html
from newutils.vulnerabilities import (
    get_missing_dependency,
    ignore_advisories,
)
from typing import (
    Any,
    Optional,
)
from uuid import (
    uuid4 as uuid,
)


async def get_finding(loaders: Dataloaders, finding_id: str) -> Finding:
    finding = await loaders.finding.load(finding_id)
    if finding is None:
        raise FindingNotFound()

    return finding


def get_hash(
    specific: str, type_: str, where: str, root_id: Optional[str] = None
) -> int:
    # Return a unique identifier according to the business rules
    items: tuple[str, ...] = (specific, type_, where)
    if root_id:
        items = (*items, root_id)
    return hash(items)


async def get_hash_from_machine_vuln(
    loaders: Dataloaders, vuln: Vulnerability
) -> int:
    if (
        vuln.hacker_email
        not in (
            "machine@fluidattacks.com",
            "kamado@fluidattacks.com",
        )
        or vuln.skims_method is None
    ):
        raise InvalidParameter()
    finding = await get_finding(loaders, vuln.finding_id)
    return int.from_bytes(
        hashlib.sha256(
            bytes(
                (
                    get_path_from_integrates_vulnerability(
                        vuln.state.where, vuln.type, ignore_cve=True
                    )[1]
                    + vuln.state.specific
                    + finding.title.split(".")[0]
                    + vuln.skims_method
                    # if you want to add a field to the hash you must
                    # also do it in the skims function
                    + (
                        get_missing_dependency(vuln.state.where)
                        if vuln.skims_method
                        == "python.pip_incomplete_dependencies_list"
                        else ""
                    )
                ),
                encoding="utf-8",
            )
        ).digest()[:8],
        "little",
    )


def get_hash_from_dict(vuln: dict[str, Any]) -> int:
    nonce: str = uuid().hex
    specific = vuln.get("specific", nonce)
    type_ = vuln.get("vuln_type", nonce)
    where = vuln.get("where", nonce)
    return get_hash(specific=specific, type_=type_, where=where)


def get_path_from_integrates_vulnerability(
    vulnerability_where: str,
    vulnerability_type: VulnerabilityType,
    ignore_cve: bool = False,
) -> tuple[str, str]:
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
    email: str,
    group_name: str,
) -> str:
    is_manager = await authz.get_group_level_role(
        loaders, email, group_name
    ) in {"user_manager", "customer_manager", "vulnerability_manager"}
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
) -> set[str]:
    # If a vuln is linked to a root, return it
    # otherwise return all roots, the vuln must belong to one of them
    root_nicknames: set[str] = set()

    root_ids: tuple[str, ...] = tuple(
        vulnerability.root_id
        for vulnerability in vulnerabilities
        if vulnerability.root_id
    )
    if len(vulnerabilities) == len(root_ids):
        non_duplicate_root_ids: set[str] = set(root_ids)
        root_nicknames.update(
            root.state.nickname
            for root in await loaders.group_roots.load(group)
            if root.id in non_duplicate_root_ids
        )
    else:
        root_nicknames.update(
            root.state.nickname
            for root in await loaders.group_roots.load(group)
            if isinstance(root, GitRoot)
        )

    return root_nicknames


def format_vulnerability_locations(where: list[str]) -> str:
    location_str: str = ""
    for location in set(where):
        location_str += f"{location}\n"
    return location_str
