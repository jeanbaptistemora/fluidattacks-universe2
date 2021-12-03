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
def allows_all_outbound_traffic(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
            "aws_security_group",
        ],
        exclude=exclude,
    ):

        security_groups_egress = res_props.get("egress", [])

        if not security_groups_egress:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity="aws_security_group",
                    identifier=res_name,
                    reason="allows all outbound traffic",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 security groups allows all outbound traffic",
        msg_closed="EC2 security groups do not allow all outbound traffic",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ip_protocols(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with any ip protocol.

    The following checks are performed:

    * W40 Security Groups egress with an IpProtocol of -1 found
    * W42 Security Groups ingress with an ipProtocol of -1 found

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=["aws_security_group", "aws_security_group_rule"],
        exclude=exclude,
    ):
        rules = _tipify_rules(res_props)
        for rule in rules:
            if str(rule.get("protocol")) == "-1":
                vuln = Vulnerability(
                    path=yaml_path,
                    entity=f'{rule.get("type")}/protocol/-1',
                    identifier=res_name,
                    reason="Authorize all IP protocols",
                )
                vulnerabilities.append(vuln)
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=(
            "EC2 security groups have ingress/egress rules "
            "with unrestricted IP protocols"
        ),
        msg_closed=(
            "EC2 security groups do not have ingress/egress rules "
            "with unrestricted IP protocols"
        ),
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ports(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Avoid ``aws_security_group`` ingress/egress rules with port ranges.

    The following checks are performed:

    * W27 Security Groups found ingress with port range
        instead of just a single port
    * W29 Security Groups found egress with port range
        instead of just a single port

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
        resource_types=["aws_security_group", "aws_security_group_rule"],
        exclude=exclude,
    ):
        rules = _tipify_rules(res_props)
        for rule in rules:
            from_port, to_port = rule.get("from_port"), rule.get("to_port")
            if int(from_port) < int(to_port):
                vuln = Vulnerability(
                    path=yaml_path,
                    entity=f'{rule.get("type")}/from_port->to_port/'
                    f"{from_port}->{to_port}",
                    identifier=res_name,
                    reason="Grants access over a port range",
                )
                vulnerabilities.append(vuln)
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=(
            "EC2 security groups have ingress/egress rules "
            "that allow access over a range of ports"
        ),
        msg_closed=(
            "EC2 security groups have ingress/egress rules "
            "that allow access over single ports"
        ),
    )


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


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_an_iam_instance_profile(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Verify if ``aws_instance`` uses an iam_instance_profile.

    EC2 instances need credentials to access other AWS services.

    An IAM role attached to the instance provides these credentials in a secure
    way. With this, you don't have to manage credentials because they are
    temporarily provided by the IAM Role and are rotated automatically.

    See: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide
    /iam-roles-for-amazon-ec2.html

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not attached an
                iam_instance_profile.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_instance",
        ],
        exclude=exclude,
    ):

        if "iam_instance_profile" not in res_props:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity="aws_instance/iam_instance_profile",
                    identifier=res_name,
                    reason="is not present",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 instances have not an iam_instance_profile set",
        msg_closed="EC2 instances have an iam_instance_profile set",
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def is_associate_public_ip_address_enabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Verify if ``aws_instance`` has assigned public IPs.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if instance's **NetworkInterfaces** attribute has the
                **AssociatePublicIpAddress** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=["aws_instance", "aws_launch_template"],
        exclude=exclude,
    ):
        if res_props["type"] == "aws_launch_template":
            public_ip = helper.to_boolean(
                res_props.get("network_interfaces", []).get(
                    "associate_public_ip_address", False
                )
            )
        else:
            public_ip = helper.to_boolean(
                res_props.get("associate_public_ip_address", False)
            )

        if public_ip:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(
                        f'{res_props["type"]}/'
                        "associate_public_ip_address/"
                        f"{public_ip}"
                    ),
                    identifier=res_name,
                    reason="associates public IP on launch",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 instances will be launched with public ip addresses",
        msg_closed="EC2 instances won't be launched with public ip addresses",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_default_security_group(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Verify if ``EC2`` has no **security_groups** explicitely set.

    By default EC2 Instances that do not specify
    **security_groups** or **vpc_security_group_ids** are launched
    with the default security group (allow all).

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not the **security_groups** or
                **vpc_security_group_ids** parameters set.
                (Either in the **aws_launch_template** or in the
                **aws_instance** entities)
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=["aws_instance", "aws_launch_template"],
        exclude=exclude,
    ):
        launch_template_sgs = res_props.get("security_groups", [])
        launch_template_sgs_ids = res_props.get("vpc_security_group_ids", [])

        if launch_template_sgs or launch_template_sgs_ids:
            # Not vulnerable
            continue

        vulnerabilities.append(
            Vulnerability(
                path=yaml_path,
                entity=(f'{res_props["type"]}/' "(vpc)_security_groups(_ids)"),
                identifier=res_name,
                reason="is empty, and therefore uses default security group",
            )
        )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=(
            "EC2 Instances or Launch Templates are using the default"
            " security group"
        ),
        msg_closed=(
            "EC2 Instances or Launch Templates are not using the "
            "default security group"
        ),
    )
