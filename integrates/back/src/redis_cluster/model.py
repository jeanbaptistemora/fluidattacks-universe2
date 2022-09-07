# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Dict,
    Set,
)

# Constants
ENTITIES: Dict[str, Dict[str, Set[str]]] = dict(
    analytics=dict(
        args={
            "id",
        },
        attrs={
            "document",
            "graphics_report",
        },
        dependencies={
            "revoke_analytics",
        },
    ),
    authz_group=dict(
        args={
            "name",
        },
        attrs={
            "policies",
        },
        dependencies={
            "revoke_authz_group",
        },
    ),
    authz_subject=dict(
        args={
            "id",
        },
        attrs={
            "policies",
        },
        dependencies={
            "revoke_authz_subject",
        },
    ),
    event=dict(
        args={
            "id",
        },
        attrs={
            "consulting",
        },
        dependencies={
            "add_event_consult",
            "reject_event_solution",
            "request_event_verification",
            "request_vulnerabilities_hold",
        },
    ),
    finding=dict(
        args={
            "id",
        },
        attrs={
            "consulting",
            "historic_state",
            "observations",
            "records",
            "vulnerabilities",
            "zero_risk",
        },
        dependencies={
            "add_finding_consult",
            "approve_draft",
            "confirm_vulnerabilities_zero_risk",
            "handle_vulnerabilities_acceptance",
            "reject_draft",
            "reject_vulnerabilities_zero_risk",
            "request_vulnerabilities_verification",
            "request_vulnerabilities_zero_risk",
            "remove_finding",
            "remove_finding_evidence",
            "remove_vulnerability",
            "remove_vulnerability_tags",
            "submit_draft",
            "update_evidence",
            "update_evidence_description",
            "update_finding_description",
            "update_severity",
            "update_vulnerability_treatment",
            "update_vulnerability_commit",
            "update_vulnerabilities_treatment",
            "upload_file",
            "verify_vulnerabilities_request",
        },
    ),
    forces_execution=dict(
        args={
            "group",
            "id",
        },
        attrs={
            "forces_execution",
        },
        dependencies=set(),
    ),
    group=dict(
        args={
            "name",
        },
        attrs={
            "consulting",
            "last_closed_vulnerability_finding",
            "max_open_severity_finding",
            "max_severity",
            "max_severity_finding",
            "stakeholders",
            "total_findings",
        },
        dependencies={
            "add_event",
            "add_group_consult",
            "add_group_tags",
            "approve_draft",
            "confirm_access",
            "grant_stakeholder_access",
            "reject_access",
            "remove_finding",
            "remove_group",
            "remove_group_tag",
            "remove_stakeholder_access",
            "solve_event",
            "unsubscribe_from_group",
            "update_severity",
            "upload_file",
            "update_group",
            "update_group_stakeholder",
            "update_vulnerabilities_treatment",
            "verify_vulnerabilities_request",
        },
    ),
    organization=dict(
        args={
            "id",
        },
        attrs={
            "stakeholders",
        },
        dependencies={
            "add_stakeholder",
            "confirm_access",
            "confirm_access_organization",
            "update_organization_stakeholder",
            "grant_stakeholder_organization_access",
            "reject_access_organization",
            "remove_stakeholder_organization_access",
            "unsubscribe_from_group",
        },
    ),
    session=dict(
        args={
            "email",
        },
        attrs={
            "jti",
            "jwt",
            "web",
        },
        dependencies={
            "session_logout",
        },
    ),
    groups=dict(
        args=set(),
        attrs={
            "forces",
        },
        dependencies=set(),
    ),
)


class KeyNotFound(Exception):
    pass


def build_key(entity: str, attr: str, **args: str) -> str:
    if entity not in ENTITIES:
        raise ValueError(f"Invalid entity: {entity}")

    if attr not in ENTITIES[entity]["attrs"]:
        raise ValueError(f"Invalid attr: {entity}.{attr}")

    extra_args: Set[str] = set(args) - ENTITIES[entity]["args"]
    if extra_args:
        raise ValueError(f"Extra args for {entity}.{attr}: {extra_args}")

    missing_args: Set[str] = ENTITIES[entity]["args"] - set(args)
    if missing_args:
        raise ValueError(f"Missing args for {entity}.{attr}: {missing_args}")

    # >>> build_key('a', 'b', c=1, d=2)
    # 'a.b@c=1,d=2
    key: str = f"{entity}.{attr}@" + ",".join(
        sorted(f"{k}={v}" for k, v in args.items())
    )

    return key


def build_keys_by_dependencies(dependency: str, **args: str) -> Set[str]:
    keys: Set[str] = set()
    for key, value in ENTITIES.items():
        if dependency in value["dependencies"]:
            required_args: Dict[str, str] = {
                arg_base: arg_value
                for arg, arg_value in args.items()
                for arg_base in [arg.replace(f"{key}_", "")]
                if arg_base in value["args"]
            }

            keys.update(build_keys_for_entity(key, **required_args))

    # >>> get_keys_to_delete('delete_vulnerability_tags', finding_id=123)
    # {'finding.verified@id=123', 'finding.open_vulns@id=123',
    #  'finding.age@id=123', 'finding.observations@id=123',
    #  'finding.ports_vulns@id=123', 'finding.closed_vulns@id=123',
    #  'finding.inputs_vulns@id=123', 'finding.lines_vulns@id=123',
    #  'finding.vulns@id=123', 'finding.exploit@id=123'}
    return keys


def build_keys_for_entity(entity: str, **args: str) -> Set[str]:
    keys: Set[str] = {
        build_key(entity, attr, **args) for attr in ENTITIES[entity]["attrs"]
    }
    return keys
