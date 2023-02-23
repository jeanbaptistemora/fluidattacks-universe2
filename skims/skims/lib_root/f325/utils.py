from aws.services import (
    ACTIONS_NEW,
)
from contextlib import (
    suppress,
)
from lib_root.utilities.terraform import (
    get_attribute,
    get_list_from_node,
)
from model.graph_model import (
    Graph,
    NId,
)
import re


def has_attribute_wildcard(attribute: str | list) -> bool:
    result: bool = False
    for value in attribute if isinstance(attribute, list) else [attribute]:
        if value == "*":
            result = True
            break
    return result


def has_write_actions(actions: str | list) -> bool:
    result: bool = False
    for entry in actions if isinstance(actions, list) else [actions]:
        with suppress(ValueError):
            service, action = entry.split(":")
            if service in ACTIONS_NEW:
                if (
                    "*" in action
                    and len(
                        [
                            act
                            for act in ACTIONS_NEW[service].get("write", [])
                            if re.match(action.replace("*", ".*"), act)
                            and act
                            not in ACTIONS_NEW[service].get(
                                "wildcard_resource", []
                            )
                        ]
                    )
                    > 0
                ):
                    result = True
                    break
                if action in ACTIONS_NEW[service].get(
                    "write", []
                ) and action not in ACTIONS_NEW[service].get(
                    "wildcard_resource", []
                ):
                    result = True
                    break
    return result


def _policy_has_excessive_permissions(stmt: dict) -> bool:
    has_excessive_permissions: bool = False
    effect = stmt.get("Effect")
    if effect == "Allow":
        actions = stmt.get("Action", [])
        resource = stmt.get("Resource", [])
        if stmt.get("NotAction", []) or stmt.get("NotResource", []):
            has_excessive_permissions = True
        if has_attribute_wildcard(resource) and (
            has_attribute_wildcard(actions) or has_write_actions(actions)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions


def _policy_has_excessive_permissions_policy_document(
    graph: Graph, stmt: NId
) -> bool:
    has_excessive_permissions: bool = False
    effect, effect_val, _ = get_attribute(graph, stmt, "effect")
    if effect_val == "Allow" or effect is None:
        _, _, action_id = get_attribute(graph, stmt, "actions")
        _, _, resources_id = get_attribute(graph, stmt, "resources")
        action_list = get_list_from_node(graph, action_id)
        resources_list = get_list_from_node(graph, resources_id)
        if (
            get_attribute(graph, stmt, "not_actions")[0]
            or get_attribute(graph, stmt, "not_resources")[0]
        ):
            has_excessive_permissions = True
        if has_attribute_wildcard(resources_list) and (
            has_attribute_wildcard(action_list)
            or has_write_actions(action_list)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions


def _policy_has_excessive_permissions_json_encode(
    graph: Graph, stmt: NId
) -> bool:
    has_excessive_permissions: bool = False
    _, effect_val, _ = get_attribute(graph, stmt, "Effect")
    if effect_val == "Allow":
        _, _, action_id = get_attribute(graph, stmt, "Action")
        _, _, resources_id = get_attribute(graph, stmt, "Resource")
        action_list = get_list_from_node(graph, action_id)
        resources_list = get_list_from_node(graph, resources_id)
        if (
            get_attribute(graph, stmt, "NotAction")[0]
            or get_attribute(graph, stmt, "NotResource")[0]
        ):
            has_excessive_permissions = True
        if has_attribute_wildcard(resources_list) and (
            has_attribute_wildcard(action_list)
            or has_write_actions(action_list)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions
