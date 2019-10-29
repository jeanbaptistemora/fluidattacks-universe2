# -*- coding: utf-8 -*-

"""AWS cloud checks (RDS)."""

# local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.cloud.cloudformation import (
    _get_result_as_tuple,
    Vulnerability,
)
from fluidasserts.helper.cloudformation import (
    to_boolean,
    iterate_resources_in_template,
    CloudFormationError,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, CloudFormationError)
def has_unencrypted_storage(template_path: str) -> tuple:
    """
    Check if any `AWS::RDS::DBInstance` uses unencrypted storage.

    :param template_path: Location of CloudFormation's template file,
        (Both YAML and JSON formats are supported :).
    :returns: - ``OPEN`` if any *RDS-DB* Instance uses unencrypted snapshots.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for res_name, res_properties in iterate_resources_in_template(
            template_path, 'AWS::RDS::DBInstance'):
        res_storage_encrypted = \
            to_boolean(res_properties['StorageEncrypted'])

        is_vulnerable: bool = not res_storage_encrypted

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template_path,
                    service='RDS',
                    identifier=res_name,
                    reason='uses unencrypted storage'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances use unencrypted storage',
        msg_closed='RDS instances use encrypted storage')
