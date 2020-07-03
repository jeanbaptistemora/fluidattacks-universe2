"""
AWS CloudFormation checks for ``IAM`` (Identity and Access Management).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# pylint: disable=too-many-branches,too-many-nested-blocks,too-many-statements
# Standard imports
import re
from typing import List, Optional, Pattern, Dict, Tuple

from networkx import DiGraph

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_resources
from fluidasserts.cloud.aws.cloudformation import has_values
from fluidasserts.cloud.aws.cloudformation import get_type
from fluidasserts.cloud.aws.cloudformation import get_value
import fluidasserts.cloud.aws.cloudformation as main


@api(risk=MEDIUM, kind=SAST)  # noqa: MC0001
@unknown_if(FileNotFoundError)
def is_role_over_privileged(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
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
    wildcard_action: Pattern = re.compile(r'^(\*)|(\w+:\*)$')
    wildcard_resource: Pattern = re.compile(r'^(\*)$')
    roles: List[int] = get_resources(graph, map(lambda x: x[0], templates),
                                     {'AWS', 'IAM', 'Role'}, info=True)

    for role, resource, template in roles:
        line: int = resource['line']
        role_name: str = resource['name']
        _managed_policies: List[int] = helper.get_index(
            get_resources(graph, role, 'ManagedPolicyArns', depth=3), 0)
        vulnerable_entities: List[str] = []
        if _managed_policies:
            managed_policies = get_resources(graph,
                                             _managed_policies,
                                             'Item',
                                             depth=4)
            for man_pol in managed_policies:
                # W43: IAM role should not have AdministratorAccess policy
                policy_arn = graph.nodes.get(man_pol)['value']
                if 'AdministratorAccess' in policy_arn:
                    entity = f'ManagedPolicyArns: {policy_arn}'
                    reason = 'grants excessive privileges'
                    line = graph.nodes.get(man_pol)['line']
                    vulnerable_entities.append((entity, reason, line))

        _policies: List[int] = helper.get_index(
            get_resources(graph, role, 'Policies', depth=3), 0)
        if _policies:
            _policy_documents = get_resources(graph,
                                              _policies,
                                              'PolicyDocument',
                                              depth=4)
            for pol_doc in _policy_documents:
                _statements = get_resources(graph,
                                            pol_doc,
                                            'Statement',
                                            depth=5)
                statements = get_resources(graph,
                                           _statements,
                                           'Item',
                                           depth=6)
                for statement in statements:
                    effect = helper.get_index(get_resources(graph,
                                                            statement,
                                                            'Effect',
                                                            depth=7), 0)
                    res = helper.get_index(get_resources(graph,
                                                         statement,
                                                         'Resource',
                                                         depth=7), 0)
                    not_res = helper.get_index(get_resources(graph,
                                                             statement,
                                                             'NotResource',
                                                             depth=7), 0)
                    _actions = helper.get_index(get_resources(graph,
                                                              statement,
                                                              'Action',
                                                              depth=7), 0)
                    if _actions:
                        actions = get_resources(graph,
                                                _actions,
                                                'Item',
                                                depth=7)
                    else:
                        actions = []
                    _not_actions = helper.get_index(get_resources(graph,
                                                                  statement,
                                                                  'NotAction',
                                                                  depth=7), 0)

                    if effect:
                        effect_val = get_value(graph, effect)
                        if effect_val != 'Allow':
                            continue

                    if _not_actions:
                        # W15: IAM role should not allow Allow+NotAction
                        entity = 'Policies/PolicyDocument/Statement/NotAction'
                        reason = 'avoid security through black listing'
                        line = graph.nodes.get(_not_actions)['line']
                        vulnerable_entities.append((entity, reason, line))
                    # W21: IAM role should not allow Allow+NotResource
                    if not_res:
                        entity = ('Policies/PolicyDocument/'
                                  'Statement/NotResource')
                        reason = 'avoid security through black listing'
                        line = graph.nodes.get(not_res)['line']
                        vulnerable_entities.append((entity, reason, line))

                    for action in actions:
                        act_val = get_value(graph, action)
                        # F3: IAM role should not allow * action on its
                        #   permissions policy
                        if wildcard_action.match(act_val):
                            entity = (f'Policies/PolicyDocument'
                                      f'/Statement/Action: {act_val}')
                            reason = 'grants wildcard privileges'
                            line = graph.nodes.get(action)['line']
                            vulnerable_entities.append((entity, reason, line))

                    # W11: IAM role should not allow * resource on its
                    #   permissions policy
                    # F38: IAM role should not allow * resource with
                    #   PassRole action on its permissions policy
                    if res:
                        res_val = get_value(graph, res)
                        if res_val:  # Resources may be a value or a list
                            if wildcard_resource.match(get_value(graph, res)):
                                entity = (f'Policies/PolicyDocument'
                                          f'/Statement/Resource: {res_val}')
                                reason = 'grants wildcard privileges'
                                line = graph.nodes.get(res)['line']
                                vulnerable_entities.append((entity,
                                                            reason,
                                                            line))
                        else:
                            res_list = get_resources(graph,
                                                     res,
                                                     'Item',
                                                     depth=7)
                            for rsrc in res_list:
                                res_val = get_value(graph, rsrc)
                                if wildcard_resource.match(res_val):
                                    entity = (f'Policies/PolicyDocument'
                                              f'/Statement/Resource:{res_val}')
                                    reason = 'grants wildcard privileges'
                                    line = graph.nodes.get(rsrc)['line']
                                    vulnerable_entities.append((entity,
                                                                reason,
                                                                line))

        _assume_role_policy: List[int] = helper.get_index(
            get_resources(graph, role, 'AssumeRolePolicyDocument', depth=3), 0)
        if _assume_role_policy:
            _statements = get_resources(graph,
                                        _assume_role_policy,
                                        'Statement',
                                        depth=4)
            statements = get_resources(graph,
                                       _statements,
                                       'Item',
                                       depth=5)
            for statement in statements:
                effect = helper.get_index(get_resources(graph,
                                                        statement,
                                                        'Effect',
                                                        depth=6), 0)
                not_princ = helper.get_index(get_resources(graph,
                                                           statement,
                                                           'NotPrincipal',
                                                           depth=6), 0)
                _actions = helper.get_index(get_resources(graph,
                                                          statement,
                                                          'Action',
                                                          depth=6), 0)
                if _actions:
                    actions = get_resources(graph,
                                            _actions,
                                            'Item',
                                            depth=6)
                else:
                    actions = []
                _not_actions = helper.get_index(get_resources(graph,
                                                              statement,
                                                              'NotAction',
                                                              depth=7), 0)

                if effect:
                    effect_val = get_value(graph, effect)
                    if effect_val != 'Allow':
                        continue

                if _not_actions:
                    # W15: IAM role should not allow Allow+NotAction
                    entity = 'AssumeRolePolicyDocument/Statement/NotAction'
                    reason = 'avoid security through black listing'
                    line = graph.nodes.get(_not_actions)['line']
                    vulnerable_entities.append((entity, reason, line))
                # W21: IAM role should not allow Allow+NotResource
                if not_princ:
                    entity = ('AssumeRolePolicyDocument/'
                              'Statement/NotPrincipal')
                    reason = 'avoid security through black listing'
                    line = graph.nodes.get(not_princ)['line']
                    vulnerable_entities.append((entity, reason, line))

                for action in actions:
                    act_val = get_value(graph, action)
                    # F3: IAM role should not allow * action on its
                    #   permissions policy
                    if wildcard_action.match(act_val):
                        entity = (f'AssumeRolePolicyDocument'
                                  f'/Statement/Action: {act_val}')
                        reason = 'grants wildcard privileges'
                        line = graph.nodes.get(action)['line']
                        vulnerable_entities.append((entity, reason, line))
        if vulnerable_entities:
            for entity, reason, line in set(vulnerable_entities):
                vulnerabilities.append(
                    Vulnerability(
                        path=template['path'],
                        entity=f'AWS::IAM::Role/{entity}',
                        identifier=role_name,
                        line=line,
                        reason=reason)
                )
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='IAM Role grants unnecessary privileges',
        msg_closed='IAM Role grants granular privileges')


def _is_generic_policy_miss_configured(  # noqa: MC0001
        path: str, exclude: Optional[List[str]], resource: str) -> tuple:
    """Policy and ManagedPolicy are equal in its PolicyDocument, reuse code."""
    vulnerabilities: List[Vulnerability] = []
    wildcard_action: Pattern = re.compile(r'^(\*)|(\w+:\*)$')
    wildcard_resource: Pattern = re.compile(r'^(\*)$')

    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    resources: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'IAM', resource},
        info=True)
    for res, res_node, template in resources:
        vulnerable_entities = []
        policy_document: int = get_resources(
            graph, res, 'PolicyDocument', depth=8)
        if not policy_document:
            continue

        effects = has_values(graph, policy_document, 'Effect', 'Allow', 4)
        for effect in effects:
            father = list(graph.predecessors(effect))[0]
            # W16: IAM policy should not allow Allow+NotAction
            # W17: IAM managed policy should not allow Allow+NotAction
            no_action = helper.get_index(
                get_resources(graph, father, 'NotAction', depth=3), 0)
            if no_action:
                entity = f'{resource}/PolicyDocument/Statement/NotAction'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason,
                                            graph.nodes[no_action]['line']))
            # W22: IAM policy should not allow Allow+NotResource
            # W23: IAM managed policy should not allow Allow+NotResource
            no_resource = helper.get_index(
                get_resources(graph, father, 'NotResource', depth=3), 0)
            if no_resource:
                entity = f'{resource}/PolicyDocument/Statement/NotResource'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason,
                                            graph.nodes[no_resource]['line']))

            action_node = helper.get_index(
                get_resources(graph, father, 'Action'), 0)
            for _action in main.get_ref_nodes(
                    graph, action_node, condition=wildcard_action.match,
                    depth=6) + [action_node] if action_node else []:
                # F4: IAM policy should not allow * action
                # F5: IAM managed policy should not allow * action
                _action_node = graph.nodes[_action]
                if 'value' not in _action_node:
                    continue
                entity = (f'{resource}/PolicyDocument'
                          f'/Statement/Action: {_action_node["value"]}')
                reason = 'grants wildcard privileges'
                vulnerable_entities.append((entity, reason,
                                            _action_node['line']))

            _resources_node = helper.get_index(
                get_resources(graph, father, 'Resource'), 0)
            for _resource in main.get_ref_nodes(
                    graph, _resources_node, condition=wildcard_resource.match,
                    depth=6) + [_resources_node] if _resources_node else []:
                # W12: IAM policy should not allow * resource
                # W13: IAM managed policy should not allow * resource
                # F39: IAM policy should not allow * resource with
                #   PassRole action
                # F40: IAM managed policy should not allow a * resource with
                #   PassRole action
                _resource_node = graph.nodes[_resource]
                if 'value' not in _resource_node:
                    continue
                entity = (f'{resource}/PolicyDocument'
                          f'/Statement/Resource: {_resource_node["value"]}')
                reason = 'grants wildcard privileges'
                vulnerable_entities.append((entity, reason,
                                            _resource_node['line']))

        users: int = helper.get_index(
            get_resources(graph, res, 'Users', depth=3), 0)
        for user in main.get_ref_nodes(
                graph, users, lambda x: isinstance(x, str)) if users else []:
            user_node = graph.nodes[user]
            entity = f'{resource}/Users: {user_node["value"]}'
            reason = f'{resource} applied to user, apply to role instead'
            vulnerable_entities.append((entity, reason, user_node['line']))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'AWS::IAM::{resource}/{entity}',
                    identifier=res_node["name"],
                    line=line,
                    reason=reason)
                for entity, reason, line in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=f'IAM {resource} is miss configured',
        msg_closed=f'IAM {resource} is properly configured')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_policy_miss_configured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::Policy`` is miss configured.

    The following checks are performed:

    * F4 IAM policy should not allow * action
    * F11 IAM policy should not apply directly to users.
        Should be on group
    * F39 IAM policy should not allow * resource with PassRole action
    * W12 IAM policy should not allow * resource
    * W16 IAM policy should not allow Allow+NotAction
    * W22 IAM policy should not allow Allow+NotResource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_generic_policy_miss_configured(
        path=path, exclude=exclude, resource='Policy')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_managed_policy_miss_configured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::ManagedPolicy`` is miss configured.

    The following checks are performed:

    * F5 IAM managed policy should not allow * action
    * F12 IAM managed policy should not apply directly to users.
        Should be on group
    * F40 IAM managed policy should not allow a * resource with PassRole action
    * W13 IAM managed policy should not allow * resource
    * W17 IAM managed policy should not allow Allow+NotAction
    * W23 IAM managed policy should not allow Allow+NotResource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_generic_policy_miss_configured(
        path=path, exclude=exclude, resource='ManagedPolicy')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def missing_role_based_security(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::User`` is granted privileges but not through a Role.

    The following checks are performed:

    * F10 IAM user should not have any inline policies.
        Should be centralized Policy object on group (Role)

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    reason = ('do not attach inline policies'
              '; use role-based access control')

    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    users: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'IAM', 'User'},
        info=True)
    for user, resource, template in users:
        vulnerable_entities = []
        policies: int = get_resources(graph, user, 'Policies', depth=2)
        items = get_resources(graph, policies, 'Item')
        for policy in items:
            line = graph.nodes[policy]['line']
            policy_name_value: str = 'any'
            policy_name: int = helper.get_index(
                get_resources(graph, policy, 'PolicyName', depth=4), 0)
            if not policy_name:
                policy_name = helper.get_index(
                    get_resources(graph, policy, 'Ref', depth=4), 0)
            if policy_name:
                line = graph.nodes[policy_name]['line']
                policy_name_value = graph.nodes[policy_name].get(
                    'value', 'any')

            entity = f'Policies: {policy_name_value}'
            vulnerable_entities.append((entity, line))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'AWS::IAM::User/{entity}',
                    identifier=resource['name'],
                    line=line,
                    reason=reason)
                for entity, line in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='IAM User is not assigned permissions through a role',
        msg_closed='IAM User is assigned permissions through a role')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_wildcard_resource_on_write_action(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if write actions are allowed on all resources.

    Do not allow ``"Resource": "*"`` to have write actions.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    documents: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'IAM', 'ManagedPolicy', 'Role'},
        info=True,
        num_labels=3)
    for doc, resource, template in documents:
        type_: str = "AWS::IAM::" + get_type(graph, doc,
                                             {'ManagedPolicy', 'Role'})
        vulnerable_lines: List[str] = []
        policy_documents: int = get_resources(
            graph, doc, 'PolicyDocument', depth=8)
        if not policy_documents:
            continue
        for policy in policy_documents:
            statement = get_resources(graph, policy, 'Statement')[0]
            if main.policy_statement_privilege(graph, statement, 'Allow',
                                               'write'):
                vulnerable_lines.append(graph.nodes[statement]['line'])

        if vulnerable_lines:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'{type_}/PolicyDocument',
                    identifier=resource['name'],
                    line=line,
                    reason='allows write actions on a wildcard resource.')
                for line in vulnerable_lines)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Write actions are allowed for all resources.',
        msg_closed='Write actions are not allowed for all resources.')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_privileges_over_iam(path: str,
                            exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if a policy documents has privileges over iam.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any policy documents has privileges over iam.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    documents: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'IAM', 'ManagedPolicy', 'Role'},
        info=True,
        num_labels=3)
    for doc, resource, template in documents:
        type_: str = "AWS::IAM::" + get_type(graph, doc,
                                             {'ManagedPolicy', 'Role'})
        vulnerable_lines: List[str] = []
        policy_documents: int = get_resources(
            graph, doc, 'PolicyDocument', depth=8)
        if not policy_documents:
            continue
        for policy in policy_documents:
            statement = get_resources(graph, policy, 'Statement')[0]
            if helper.service_is_present_statement_(graph, statement, 'Allow',
                                                    'iam'):
                vulnerable_lines.append(graph.nodes[statement]['line'])

        if vulnerable_lines:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'{type_}/PolicyDocument',
                    identifier=resource['name'],
                    line=line,
                    reason='has privileges over iam.')
                for line in vulnerable_lines)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Policies have privileges over iam.',
        msg_closed='Policies have no privileges over iam.')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_full_access_to_ssm(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if there are policy documents that allow full access to ssm agent.

    SSM allows everyone with access to run commands as root on EC2 instances

    https://cloudonaut.io/aws-ssm-is-a-trojan-horse-fix-it-now/

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    documents: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {
            'AWS', 'IAM', 'ManagedPolicy', 'Policy', 'Role'},
        info=True, num_labels=3)
    for doc, resource, template in documents:
        type_: str = "AWS::IAM::" + \
            get_type(graph, doc, {'ManagedPolicy', 'Policy', 'Role'})
        reason: str = 'allows full access to SSM.'
        vulnerable_lines: List[int] = []
        policy_document: int = helper.get_index(get_resources(
            graph, doc, 'PolicyDocument', depth=8), 0)
        if not policy_document:
            continue

        effects = has_values(graph, policy_document, 'Effect', 'Allow', 4)
        for effect in effects:
            vulnerable = False
            father = graph.predecessors(effect)
            action = helper.get_index(
                get_resources(graph, father, 'Action'), 0)
            if action:
                vulnerable = [graph.nodes[node]['line'] for node in has_values(
                    graph, action, 'Item', 'ssm:*', depth=4)]
            if vulnerable:
                vulnerable_lines.extend(vulnerable)
        if vulnerable_lines:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'{type_}/PolicyDocument',
                    identifier=resource['name'],
                    line=line,
                    reason=reason) for line in vulnerable_lines)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Policy allows full access to SSM.',
        msg_closed='Policy does not allow full access to SSM.')
