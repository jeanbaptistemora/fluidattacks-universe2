# Standard library
from typing import (
    Dict,
    Set,
)


# Constants
ENTITIES: Dict[str, Dict[str, Set[str]]] = dict(
    analytics=dict(
        args={
            'id',
        },
        attrs={
            'document',
            'graphics_report',
        },
        dependencies={
            'revoke_analytics',
        },
    ),
    authz_group=dict(
        args={
            'name',
        },
        attrs={
            'policies',
        },
        dependencies={
            'revoke_authz_group',
        },
    ),
    authz_subject=dict(
        args={
            'id',
        },
        attrs={
            'policies',
        },
        dependencies={
            'revoke_authz_subject',
        },
    ),
    event=dict(
        args={
            'id',
        },
        attrs={
            'consulting',
        },
        dependencies={
            'add_event_consult',
        },
    ),
    finding=dict(
        args={
            'id',
        },
        attrs={
            'age',
            'closed_vulns',
            'consulting',
            'inputs_vulns',
            'last_vulnerability',
            'lines_vulns',
            'new_remediated',
            'observations',
            'open_age',
            'open_vulns',
            'ports_vulns',
            'records',
            'state',
            'tracking',
            'verified',
            'vulnerabilities',
            'zero_risk',
        },
        dependencies={
            'add_finding_consult',
            'approve_draft',
            'confirm_zero_risk_vuln',
            'delete_finding',
            'delete_vulnerability',
            'delete_vulnerability_tags',
            'handle_vulns_acceptation',
            'reject_draft',
            'reject_zero_risk_vuln',
            'request_verification_vulnerability',
            'request_zero_risk_vuln',
            'remove_finding_evidence',
            'submit_draft',
            'update_evidence',
            'update_evidence_description',
            'update_finding_description',
            'update_severity',
            'update_treatment_vulnerability',
            'update_vulns_treatment',
            'upload_file',
            'verify_request_vulnerability',
        },
    ),
    forces_execution=dict(
        args={
            'group',
            'id',
        },
        attrs={
            'forces_execution',
        },
        dependencies=set(),
    ),
    group=dict(
        args={
            'name',
        },
        attrs={
            'consulting',
            'last_closing_vuln_finding',
            'max_open_severity_finding',
            'max_severity',
            'max_severity_finding',
            'stakeholders',
            'toe_lines',
            'total_findings',
        },
        dependencies={
            'add_group_consult',
            'add_group_tags',
            'approve_draft',
            'confirm_access',
            'create_event',
            'delete_finding',
            'edit_group',
            'edit_stakeholder',
            'grant_stakeholder_access',
            'remove_group',
            'remove_group_tag',
            'remove_stakeholder_access',
            'solve_event',
            'unsubscribe_from_group',
            'update_severity',
            'update_vulns_treatment',
            'upload_file',
            'verify_request_vulnerability',
        },
    ),
    organization=dict(
        args={
            'id',
        },
        attrs={
            'stakeholders',
        },
        dependencies={
            'confirm_access',
            'edit_stakeholder_organization',
            'grant_stakeholder_organization_access',
            'remove_stakeholder_organization_access',
            'unsubscribe_from_group',
        },
    ),
    session=dict(
        args={
            'email',
        },
        attrs={
            'jti',
            'jwt',
            'web',
        },
        dependencies={
            'session_logout',
        },
    ),
    projects=dict(
        args=set(),
        attrs={
            'forces',
        },
        dependencies=set()
    )
)


class KeyNotFound(Exception):
    pass


def build_key(entity: str, attr: str, **args: str) -> str:
    if entity not in ENTITIES:
        raise ValueError(f'Invalid entity: {entity}')

    if attr not in ENTITIES[entity]['attrs']:
        raise ValueError(f'Invalid attr: {entity}.{attr}')

    extra_args: Set[str] = set(args) - ENTITIES[entity]['args']
    if extra_args:
        raise ValueError(f'Extra args for {entity}.{attr}: {extra_args}')

    missing_args: Set[str] = ENTITIES[entity]['args'] - set(args)
    if missing_args:
        raise ValueError(f'Missing args for {entity}.{attr}: {missing_args}')

    # >>> build_key('a', 'b', c=1, d=2)
    # 'a.b@c=1,d=2
    key: str = f'{entity}.{attr}@' + ','.join(sorted(
        f'{k}={v}' for k, v in args.items()
    ))

    return key


def build_keys_for_entity(entity: str, **args: str) -> Set[str]:
    keys: Set[str] = {
        build_key(entity, attr, **args)
        for attr in ENTITIES[entity]['attrs']
    }

    return keys


def build_keys_by_dependencies(dependency: str, **args: str) -> Set[str]:
    keys: Set[str] = set()

    for entity in ENTITIES:
        if dependency in ENTITIES[entity]['dependencies']:
            required_args: Dict[str, str] = {
                arg_base: arg_value
                for arg, arg_value in args.items()
                for arg_base in [arg.replace(f'{entity}_', '')]
                if arg_base in ENTITIES[entity]['args']
            }

            keys.update(build_keys_for_entity(entity, **required_args))

    # >>> get_keys_to_delete('delete_vulnerability_tags', finding_id=123)
    # {'finding.verified@id=123', 'finding.open_vulns@id=123',
    #  'finding.age@id=123', 'finding.observations@id=123',
    #  'finding.ports_vulns@id=123', 'finding.closed_vulns@id=123',
    #  'finding.inputs_vulns@id=123', 'finding.lines_vulns@id=123',
    #  'finding.vulns@id=123', 'finding.exploit@id=123'}
    return keys
