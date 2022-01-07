"""
AWS Terraform checks for ``EC2`` (Elastic Cloud Compute).

Some rules were inspired by `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


import contextlib
from fluidasserts import (
    LOW,
    MEDIUM,
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
import ipaddress
from typing import (
    List,
    Optional,
)


def _any_to_list(_input):
    """Convert anything to list."""
    if isinstance(_input, (dict, str)):
        res = [_input]
    else:
        res = list(_input)
    return res


def _tipify_rules(res_props):
    rules: list = []
    if res_props.get("type") == "aws_security_group":
        for rule_type in ("ingress", "egress"):
            for rule in _any_to_list(res_props.get(rule_type, [])):
                rule["type"] = rule_type
                rules.append(rule)
    else:
        rules.append(res_props)
    return rules


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_cidrs(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``aws_security_group`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    unrestricted_ipv4 = ipaddress.IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = ipaddress.IPv6Network("::/0")
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=["aws_security_group", "aws_security_group_rule"],
        exclude=exclude,
    ):
        rules = _tipify_rules(res_props)
        entities = []
        for rule in rules:
            with contextlib.suppress(
                KeyError, ValueError, ipaddress.AddressValueError
            ):
                for ipv4 in _any_to_list(rule["cidr_blocks"]):
                    ipv4_obj = ipaddress.IPv4Network(ipv4, strict=False)
                    if ipv4_obj == unrestricted_ipv4:
                        entities.append(
                            (f"cidr_blocks/{ipv4}", "must not be 0.0.0.0/0")
                        )
                    if (
                        rule["type"] == "ingress"
                        and ipv4_obj.num_addresses > 1
                    ):
                        entities.append(
                            (f"cidr_blocks/{ipv4}", "must use /32 subnet mask")
                        )

                for ipv6 in _any_to_list(rule["ipv6_cidr_blocks"]):
                    ipv6_obj = ipaddress.IPv6Network(ipv6, strict=False)
                    if ipv6_obj == unrestricted_ipv6:
                        entities.append(
                            (f"ipv6_cidr_blocks/{ipv6}", "must not be ::/0")
                        )
                    if (
                        rule["type"] == "ingress"
                        and ipv6_obj.num_addresses > 1
                    ):
                        entities.append(
                            (
                                f"ipv6_cidr_blocks/{ipv6}",
                                "must use /32 subnet mask",
                            )
                        )

            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f"{yaml_path}/{entity}",
                    identifier=res_name,
                    reason=reason,
                )
                for entity, reason in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 security groups have unrestricted CIDRs",
        msg_closed="EC2 security groups do not have unrestricted CIDRs",
    )
