"""
AWS Terraform checks for ``IAM`` (Identity and Access Management).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
import re
import json
from typing import List, Optional, Pattern

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


def _is_generic_policy_miss_configured(  # noqa: MC0001
        policy_document: dict, policy_type: str, path: str, name: str) -> list:
    vulnerabilities: list = []
    wildcard_action: Pattern = re.compile(r'^(\*)|(\w+:\*)$')
    wildcard_resource: Pattern = re.compile(r'^(\*)$')
    vulnerable_entities: List[str] = []

    for statement in helper.force_list(policy_document.get('Statement', [])):
        if statement.get('Effect') != 'Allow':
            continue

        # W16: IAM policy should not allow Allow+NotAction
        # W17: IAM managed policy should not allow Allow+NotAction
        if 'NotAction' in statement:
            entity = f'{policy_type}/policy/Statement/NotAction'
            reason = 'avoid security through black listing'
            vulnerable_entities.append((entity, reason))
        # W22: IAM policy should not allow Allow+NotResource
        # W23: IAM managed policy should not allow Allow+NotResource
        if 'NotResource' in statement:
            entity = f'{policy_type}/policy/Statement/NotResource'
            reason = 'avoid security through black listing'
            vulnerable_entities.append((entity, reason))
        for action in map(str, helper.force_list(
                statement.get('Action', []))):
            # F4: IAM policy should not allow * action
            # F5: IAM managed policy should not allow * action
            if wildcard_action.match(action):
                entity = (f'{policy_type}/policy'
                          f'/Statement/Action: {action}')
                reason = 'grants wildcard privileges'
                vulnerable_entities.append((entity, reason))
        for _resource in map(str, helper.force_list(
                statement.get('Resource', []))):
            # W12: IAM policy should not allow * policy_type
            # W13: IAM managed policy should not allow * policy_type
            # F39: IAM policy should not allow * policy_type with
            #   PassRole action
            # F40: IAM managed policy should not allow a * policy_type with
            #   PassRole action
            if wildcard_resource.match(_resource):
                entity = (f'{policy_type}/policy'
                          f'/Statement/Resource: {_resource}')
                reason = 'grants wildcard privileges'
                vulnerable_entities.append((entity, reason))

    if vulnerable_entities:
        vulnerabilities.extend(
            Vulnerability(
                path=path,
                entity=f'{policy_type}/{entity}',
                identifier=name,
                reason=reason)
            for entity, reason in set(vulnerable_entities))
    return vulnerabilities


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_policy_miss_configured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::ManagedPolicy`` is miss configured.

    The following checks are performed:

    * F5 IAM managed policy should not allow * action
    * F12 IAM managed policy should not apply directly to users.
        Should be on group
    * F40 IAM managed policy should not allow a * policy_type with PassRole
    action
    * W13 IAM managed policy should not allow * policy_type
    * W17 IAM managed policy should not allow Allow+NotAction
    * W23 IAM managed policy should not allow Allow+NotResource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are
    ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_iam_role_policy',
                'aws_iam_group_policy',
                'aws_iam_policy',
                'aws_iam_user_policy'
            ],
            exclude=exclude):
        policy = json.loads(res_props.get('policy', '{}'))
        if res_props.get('type') == 'aws_iam_user_policy':
            vulnerabilities.append(Vulnerability(
                path=yaml_path,
                entity=res_props.get('type'),
                identifier=res_name,
                reason='Should not use User Policies, '
                       'apply Role or Group Policies instead'))
        vulnerabilities += _is_generic_policy_miss_configured(
            policy_document=policy,
            policy_type=res_props['type'],
            path=yaml_path,
            name=res_name
        )
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=f'IAM Policy is miss configured',
        msg_closed=f'IAM Policy is properly configured')
