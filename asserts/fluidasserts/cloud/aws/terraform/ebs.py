"""AWS Terraform checks for ``EBS`` (Elastic Beanstalk)."""


from fluidasserts import (
    LOW,
    SAST,
)
from fluidasserts.cloud.aws.terraform import (
    _get_result_as_tuple,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from typing import (
    List,
    Optional,
)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def default_encryption_disabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if there EBS volumes are not encrypted by default.

    Verify if ``aws_ebs_encryption_by_default``
    has the ``enabled`` attribute set to **true**.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the volume is not encrypted.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_ebs_encryption_by_default",
        ],
        exclude=exclude,
    ):
        encrypted_by_default = res_props.get("enabled", "false")
        if not helper.to_boolean(encrypted_by_default):
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity="aws_ebs_encryption_by_default",
                    identifier=res_name,
                    reason="is missing or disabled",
                )
            )
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EBS volumes are not encrypted by default",
        msg_closed="EBS volumes are encrypted by default",
    )
