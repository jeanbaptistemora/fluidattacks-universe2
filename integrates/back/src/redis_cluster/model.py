# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Dict,
    Set,
)

# Constants
ENTITIES: Dict[str, Dict[str, Set[str]]] = dict(
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
    )
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
