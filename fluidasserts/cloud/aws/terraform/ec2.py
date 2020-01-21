"""AWS Terraform checks for ``EC2`` (Elastic Cloud Compute)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple
)
from fluidasserts.utils.decorators import api, unknown_if


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
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_instance',
            ],
            exclude=exclude):
        vulns = _get_unencrypted_vulns(res_name, res_props, yaml_path)
    return _get_result_as_tuple(
        vulnerabilities=vulns,
        msg_open='EC2 volumes are not encrypted',
        msg_closed='EC2 volumes are encrypted')


def _get_unencrypted_vulns(res_name, res_props, yaml_path):
    vulnerabilities: list = []
    for vol_type in ['root_block_device', 'ebs_block_device']:
        if vol_type in res_props:
            if isinstance(res_props.get(vol_type), dict):
                volumes = [res_props.get(vol_type)]
            else:
                volumes = res_props.get(vol_type)
            for volume in volumes:
                if 'device_name' not in volume:
                    volume['device_name'] = 'unnamed'
                if 'encrypted' in volume:
                    if not helper.to_boolean(volume['encrypted']):
                        vulnerabilities.append(
                            Vulnerability(
                                path=yaml_path,
                                entity=vol_type,
                                identifier=res_name + '.' +
                                volume['device_name'],
                                reason='is not encrypted'))
    return vulnerabilities
