"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/master/LICENSE.md>`_
"""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``EC2::SecurityGroup`` allows all outbound traffic.

    The following checks are performed:

    - F1000 Missing egress rule means all traffic is allowed outbound.
        Make this explicit if it is desired configuration

    When you specify a VPC security group, Amazon EC2 creates a
    **default egress rule** that **allows egress traffic** on **all ports
    and IP protocols to any location**.

    The default rule is removed only when you specify one or more egress
    rules in the **SecurityGroupEgress** directive.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroup',
            ],
            exclude=exclude):
        security_groups_egress = res_props.get('SecurityGroupEgress', [])

        if not security_groups_egress:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::EC2::SecurityGroup',
                    identifier=res_name,
                    reason='allows all outbound traffic'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups allows all outbound traffic',
        msg_closed='EC2 security groups do not allow all outbound traffic')
