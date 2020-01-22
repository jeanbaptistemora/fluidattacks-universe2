"""AWS Terraform checks for ``EC2`` (Elastic Cloud Compute)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple
)
from fluidasserts.utils.decorators import api, unknown_if


def _dict_to_list(_input):
    """Convert anything to list."""
    if isinstance(_input, (dict, str)):
        res = [_input]
    else:
        res = list(_input)
    return res


def _get_unencrypted_vulns(res_name, res_props, yaml_path):
    vulnerabilities: list = []
    for vol_type in ['root_block_device', 'ebs_block_device']:
        if vol_type in res_props:
            volumes = _dict_to_list(res_props.get(vol_type))
            for volume in volumes:
                vol_name = volume.get('device_name', 'unnamed')
                if not helper.to_boolean(volume.get('encrypted', False)):
                    vulnerabilities.append(
                        Vulnerability(
                            path=yaml_path,
                            entity=vol_type,
                            identifier=res_name + '.' +
                            vol_name,
                            reason='is not encrypted'))
    return vulnerabilities


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_volumes(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if there are EC2 instances with unencrypted volumes.

    Verify if ``ebs_root_device`` or ``ebs_block_device``
    has the encryption attribute set to **true**.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the volume is not encrypted.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulns: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_instance',
            ],
            exclude=exclude):
        vulns += _get_unencrypted_vulns(res_name, res_props, yaml_path)
    return _get_result_as_tuple(
        vulnerabilities=vulns,
        msg_open='EC2 volumes are not encrypted',
        msg_closed='EC2 volumes are encrypted')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``aws_security_group`` allows all outbound traffic.

    The following checks are performed:

    * F1000 Missing egress rule means all traffic is allowed outbound,
        Make this explicit if it is desired configuration

    When you specify a VPC security group, Amazon EC2 creates a
    **default egress rule** that **allows egress traffic** on **all ports
    and IP protocols to any location**.

    The default rule is removed only when you specify one or more egress
    rules in the **egress** directive.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_security_group',
            ],
            exclude=exclude):

        security_groups_egress = res_props.get('egress', [])

        if not security_groups_egress:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='aws_security_group',
                    identifier=res_name,
                    reason='allows all outbound traffic'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups allows all outbound traffic',
        msg_closed='EC2 security groups do not allow all outbound traffic')
