"""
AWS CloudFormation checks for ``IAM`` (Identity and Access Management).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


from fluidasserts import (
    MEDIUM,
    SAST,
)
import fluidasserts.cloud.aws.cloudformation as main
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_resources,
    get_templates,
    get_type,
    get_value,
    has_values,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from networkx import (
    DiGraph,
)
import re
from typing import (
    Dict,
    List,
    Optional,
    Pattern,
    Tuple,
)

WILDCARD_ACTION: Pattern = re.compile(r"^(\*)|(\w+:\*)$")
WILDCARD_RESOURCE: Pattern = re.compile(r"^(\*)$")


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_role_over_privileged(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``IAM::Role`` is miss configured.

    The following checks are performed:

    * F2 IAM role should not allow * action on its trust policy
    * F3 IAM role should not allow * action on its permissions policy
    * F6 IAM role should not allow Allow+NotPrincipal in its trust policy
    * F38 IAM role should not allow * resource with PassRole action on its
        permissions policy
    * W11 IAM role should not allow * resource on its permissions policy
    * W14 IAM role should not allow Allow+NotAction on trust permissions
    * W15 IAM role should not allow Allow+NotAction
    * W21 IAM role should not allow Allow+NotResource
    * W43 IAM role should not have AdministratorAccess policy

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    roles: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "IAM", "Role"},
        info=True,
    )

    for role, resource, template in roles:
        role_name: str = resource["name"]
        _managed_policies: List[int] = helper.get_index(
            get_resources(graph, role, "ManagedPolicyArns", depth=3), 0
        )
        vulnerable_entities: List[str] = []

        vulnerable_entities += _has_admin_access(_managed_policies, graph)

        _policies: List[int] = helper.get_index(
            get_resources(graph, role, "Policies", depth=3), 0
        )
        _policy_documents = get_resources(
            graph, _policies, "PolicyDocument", depth=4
        )
        vulnerable_entities += _check_policy_documents(
            _policy_documents, graph
        )

        _assume_role_policy: List[int] = helper.get_index(
            get_resources(graph, role, "AssumeRolePolicyDocument", depth=3), 0
        )
        vulnerable_entities += _check_assume_role_policies(
            _assume_role_policy, graph
        )
        if vulnerable_entities:
            for entity, reason, line in set(vulnerable_entities):
                vulnerabilities.append(
                    Vulnerability(
                        path=template["path"],
                        entity=f"AWS::IAM::Role/{entity}",
                        identifier=role_name,
                        line=line,
                        reason=reason,
                    )
                )
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="IAM Role grants unnecessary privileges",
        msg_closed="IAM Role grants granular privileges",
    )


def _check_assume_role_policies(_assume_role_policy, graph):
    vulnerable_entities: List[str] = []
    if _assume_role_policy:
        _statements = get_resources(
            graph, _assume_role_policy, "Statement", depth=4
        )
        statements = get_resources(graph, _statements, "Item", depth=5)
        for statement in statements:
            not_princ = helper.get_index(
                get_resources(graph, statement, "NotPrincipal", depth=6), 0
            )
            _actions = helper.get_index(
                get_resources(graph, statement, "Action", depth=6), 0
            )
            if _actions:
                actions = get_resources(graph, _actions, "Item", depth=6)
            else:
                actions = []
            _not_actions = helper.get_index(
                get_resources(graph, statement, "NotAction", depth=7), 0
            )

            if not has_values(graph, statement, "Effect", "Allow"):
                continue

            vulnerable_entities += _has_not_action(
                graph, _not_actions, _assume_role_policy
            )

            vulnerable_entities += _has_not_principal(
                graph, not_princ, _assume_role_policy
            )
            vulnerable_entities += _has_wildcard_action(
                graph, actions, _assume_role_policy
            )
    return vulnerable_entities


def _check_policy_documents(_policy_documents, graph):
    vulnerable_entities: List[str] = []
    for pol_doc in _policy_documents:
        _statements = get_resources(graph, pol_doc, "Statement", depth=5)
        statements = get_resources(graph, _statements, "Item", depth=6)
        for statement in statements:
            effect = helper.get_index(
                get_resources(graph, statement, "Effect", depth=7), 0
            )
            res = helper.get_index(
                get_resources(graph, statement, "Resource", depth=7), 0
            )
            not_res = helper.get_index(
                get_resources(graph, statement, "NotResource", depth=7), 0
            )
            _actions = helper.get_index(
                get_resources(graph, statement, "Action", depth=7), 0
            )
            if _actions:
                actions = get_resources(graph, _actions, "Item", depth=7)
            else:
                actions = []
            _not_actions = helper.get_index(
                get_resources(graph, statement, "NotAction", depth=7), 0
            )

            if _is_effect_allow(graph, effect):
                continue

            vulnerable_entities += _has_not_action(
                graph, _not_actions, pol_doc
            )
            vulnerable_entities += _has_not_resource(graph, not_res, pol_doc)

            vulnerable_entities += _has_wildcard_action(
                graph, actions, pol_doc
            )

            vulnerable_entities += _has_wildcard_resource(graph, res, pol_doc)
    return vulnerable_entities


def _has_not_principal(graph, not_princ, parent):
    # W21: IAM role should not allow Allow+NotResource
    vulnerable_entities: List = []
    name: str = graph.nodes.get(parent)["name"]
    if not_princ:
        entity = f"{name}/Statement/NotPrincipal"
        reason = "avoid security through black listing"
        line = graph.nodes.get(not_princ)["line"]
        vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities


def _has_wildcard_resource(graph, res, parent):
    """W11: IAM role should not allow * resource on its
      permissions policy.
    F38: IAM role should not allow * resource with
      PassRole action on its permissions policy."""
    vulnerable_entities: List = []
    name: str = graph.nodes.get(parent)["name"]
    res_list: List = _get_resource_list(graph, res)
    for res_val, line in res_list:
        if WILDCARD_RESOURCE.match(res_val):
            entity = f"{name}/Statement/Resource:{res_val}"
            reason = "grants wildcard privileges"
            line = graph.nodes.get(res)["line"]
            vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities


def _get_resource_list(graph, res):
    """Returns a list with the statement resources."""
    ret: List = []
    if res:
        res_val = get_value(graph, res)
        line = graph.nodes.get(res)["line"]
        if res_val:
            ret = [(res_val, line)]
        else:
            res_list = get_resources(graph, res, "Item", depth=7)
            ret = [
                (get_value(graph, rsrc), graph.nodes.get(rsrc)["line"])
                for rsrc in res_list
            ]
    return ret


def _has_wildcard_action(graph, actions, parent):
    vulnerable_entities: List = []
    name: str = graph.nodes.get(parent)["name"]
    for action in actions:
        act_val = get_value(graph, action)
        # F3: IAM role should not allow * action on its
        #   permissions policy
        if WILDCARD_ACTION.match(act_val):
            entity = f"{name}/Statement/Action: {act_val}"
            reason = "grants wildcard privileges"
            line = graph.nodes.get(action)["line"]
            vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities


def _has_not_resource(graph, not_res, parent):
    # W21: IAM role should not allow Allow+NotResource
    vulnerable_entities: List = []
    name: str = graph.nodes.get(parent)["name"]
    if not_res:
        entity = f"{name}/Statement/NotResource"
        reason = "avoid security through black listing"
        line = graph.nodes.get(not_res)["line"]
        vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities


def _has_not_action(graph, not_action, parent):
    vulnerable_entities: List = []
    name: str = graph.nodes.get(parent)["name"]
    if not_action:
        # W15: IAM role should not allow Allow+NotAction
        entity = f"{name}/Statement/NotAction"
        reason = "avoid security through black listing"
        line = graph.nodes.get(not_action)["line"]
        vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities


def _is_effect_allow(graph, effect):
    if effect:
        effect_val = get_value(graph, effect)
        if effect_val != "Allow":
            return True
    return False


def _has_admin_access(_managed_policies, graph):
    vulnerable_entities: List[str] = []
    if _managed_policies:
        managed_policies = get_resources(
            graph, _managed_policies, "Item", depth=4
        )
        for man_pol in managed_policies:
            # W43: IAM role should not have AdministratorAccess policy
            policy_arn = graph.nodes.get(man_pol)["value"]
            if "AdministratorAccess" in policy_arn:
                entity = f"ManagedPolicyArns: {policy_arn}"
                reason = "grants excessive privileges"
                line = graph.nodes.get(man_pol)["line"]
                vulnerable_entities.append((entity, reason, line))
    return vulnerable_entities
