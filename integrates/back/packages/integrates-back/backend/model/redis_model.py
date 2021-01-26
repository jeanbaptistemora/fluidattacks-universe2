# Standard library
from typing import (
    Dict,
    Set,
)


# Constants
ENTITIES: Dict[str, Dict[str, Set[str]]] = dict(
    event=dict(
        args={
            'id',
        },
        attrs={
            'consulting',
        },
    ),
    finding=dict(
        args={
            'id',
        },
        attrs={
            'age',
            'closed_vulns',
            'inputs_vulns',
            'lines_vulns',
            'open_vulns',
            'ports_vulns',
            'vulns',
            'exploit',
            'observations',
            'verified',
        },
    ),
    forces_execution=dict(
        args={
            'group',
            'id',
        },
        attrs={
            'forces_execution'
        },
    ),
)
# Pending:
#   finding consulting
#   finding last_vulnerability
#   finding new_remediated
#   finding open_age
#   finding records
#   finding state
#   finding tracking
#   group consulting
#   group last_closing_vuln_finding
#   group max_open_severity_finding
#   group max_severity
#   group max_severity_finding
#   group total_findings


class KeyNotFound(Exception):
    pass


def build_key(entity: str, attr: str, **args: str) -> str:
    if entity not in ENTITIES:
        raise ValueError(f'Invalid entity: {entity}')

    if attr not in ENTITIES[entity]['attrs']:
        raise ValueError(f'Invalid attr: {entity}.{attr}')

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
