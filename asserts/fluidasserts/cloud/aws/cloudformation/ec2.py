# pylint: disable=too-many-lines
"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


import contextlib
from fluidasserts import (
    HIGH,
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_predecessor,
    get_ref_nodes,
    get_templates,
    get_type,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.helper.aws import (
    CloudFormationInvalidTypeError,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from ipaddress import (
    IPv4Network,
    IPv6Network,
)
import networkx as nx
from networkx import (
    DiGraph,
)
from networkx.algorithms import (
    dfs_preorder_nodes,
)
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


def _iterate_security_group_rules(graph: DiGraph, group: int):
    """Iterate over the different security groups entities in the template."""
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    cidrs: List[int] = [
        node
        for node in dfs_preorder_nodes(graph, group, 10)
        if graph.nodes[node]["labels"].intersection({"CidrIp", "CidrIpv6"})
    ]

    rules = []
    for cidr in cidrs:
        cidr_node = get_ref_nodes(graph, cidr, helper.is_cidr)
        if not cidr_node:
            continue
        cidr_node = cidr_node[0]

        father = list(graph.predecessors(cidr))[0]
        from_port_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(
                    graph, node, lambda y: isinstance(y, (int, float))
                )
                for node in dfs_preorder_nodes(graph, father, 1)
                if "FromPort" in graph.nodes[node]["labels"]
            ]
        )

        to_port_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(
                    graph, node, lambda y: isinstance(y, (int, float))
                )
                for node in dfs_preorder_nodes(graph, father, 1)
                if "ToPort" in graph.nodes[node]["labels"]
            ]
        )

        ip_protocol_node: Union[List[int], int] = nx.utils.flatten(
            [
                get_ref_nodes(graph, node, helper.is_ip_protocol)
                for node in dfs_preorder_nodes(graph, father, 1)
                if "IpProtocol" in graph.nodes[node]["labels"]
            ]
        )

        if not from_port_node or not to_port_node or not ip_protocol_node:
            continue

        from_port_node = from_port_node[0]
        to_port_node = to_port_node[0]
        ip_protocol_node = ip_protocol_node[0]
        _type: str = get_type(
            graph, get_predecessor(graph, cidr, allow_groups), allow_groups
        )
        rule = {
            "FromPort": from_port_node,
            "ToPort": to_port_node,
            get_type(graph, cidr, {"CidrIp", "CidrIpv6"}): cidr_node,
            "IpProtocol": ip_protocol_node,
            "type": _type,
        }
        rules.append(rule)

    return rules


def _get_securitygroups(
    graph: DiGraph, path: str, exclude: Optional[List[str]] = None
) -> List[int]:
    templates: List[int] = get_templates(graph, path, exclude)
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    return [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if graph.nodes[node]["labels"].intersection(
            {"SecurityGroup", *allow_groups}
        )
    ]


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_cidrs(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if any ``EC2::SecurityGroup`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param graph: Templates converted into a DiGraph.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    allow_groups = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[Dict] = _get_securitygroups(graph, path, exclude)
    for group in security_groups:
        template: Dict = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        resource: Dict = graph.nodes[group]
        rules: List[Dict] = _iterate_security_group_rules(graph, group)

        for rule in rules:
            cidr_ip = None
            ip_object: [Union[IPv4Network, IPv6Network]] = None
            _type: str = rule["type"]
            entities: List[Tuple] = []
            if rule.get("CidrIp", None):
                cidr_ip = rule["CidrIp"]
                ip_value = graph.nodes[rule["CidrIp"]]["value"]
                ip_object: IPv4Network = IPv4Network(ip_value, strict=False)
                if ip_object == unrestricted_ipv4:
                    entities.append(
                        (f"CidrIp/{ip_value}", "must not be 0.0.0.0/0")
                    )
                if (
                    _type == "SecurityGroupIngress"
                    and ip_object.num_addresses > 1
                ):
                    entities.append(
                        (f"CidrIp/{ip_value}", "must use /32 subnet mask")
                    )
            elif rule.get("CidrIpv6", None):
                cidr_ip = rule["CidrIpv6"]
                ip_value = graph.nodes[rule["CidrIpv6"]]["value"]
                ip_object: IPv4Network = IPv6Network(ip_value, strict=False)
                if ip_object == unrestricted_ipv6:
                    entities.append(
                        (f"CidrIpv6/{ip_value}", "must not be ::/0")
                    )
                if (
                    _type == "SecurityGroupIngress"
                    and ip_object.num_addresses > 1
                ):
                    entities.append(
                        (f"CidrIpv6/{ip_value}", "must use /128 subnet mask")
                    )

            ip_node: int = graph.nodes[cidr_ip]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )

            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"AWS::EC2::{resource_type}/{entity}'",
                    identifier=resource["name"],
                    line=ip_node["line"],
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
def has_unrestricted_ip_protocols(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
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
    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)
    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template: Dict = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        for rule in _iterate_security_group_rules(graph, group):
            _type: str = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            protocol_value: Union[str, int] = graph.nodes[rule["IpProtocol"]][
                "value"
            ]
            if protocol_value in ("-1", -1):
                vulnerabilities.append(
                    Vulnerability(
                        path=template["path"],
                        entity=(
                            f"AWS::EC2::{resource_type}/IpProtocol/"
                            f"{protocol_value}"
                        ),
                        identifier=resource["name"],
                        line=graph.nodes[rule["IpProtocol"]]["line"],
                        reason="Authorize all IP protocols",
                    )
                )

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
) -> Tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with port ranges.

    The following checks are performed:

    * W27 Security Groups found ingress with port range
        instead of just a single port
    * W29 Security Groups found egress with port range
        instead of just a single port

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    # all security groups in templates
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)
    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        rules: List[int] = _iterate_security_group_rules(graph, group)

        for rule in rules:
            entities = []
            from_port, to_port = tuple(
                map(
                    str,
                    (
                        graph.nodes[rule["FromPort"]]["value"],
                        graph.nodes[rule["ToPort"]]["value"],
                    ),
                )
            )
            if float(from_port) != float(to_port):
                entities.append(f"{from_port}->{to_port}")

            _type: str = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )

            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=(
                        f"AWS::EC2::{resource_type}/"
                        f"FromPort->ToPort/{entity}"
                    ),
                    identifier=resource["name"],
                    line=graph.nodes[rule["FromPort"]]["line"],
                    reason="Grants access over a port range",
                )
                for entity in entities
            )
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


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_volumes(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Verify if ``EC2::Volume`` has the encryption attribute set to **true**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the volume is not encrypted.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    volumes: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(
            graph.nodes[node]["labels"].intersection({"AWS", "EC2", "Volume"})
        )
        > 2
    ]

    vulnerabilities: List[Vulnerability] = []
    for volume in volumes:
        template: Dict = graph.nodes[
            get_predecessor(graph, volume, "CloudFormationTemplate")
        ]
        resource: Dict = graph.nodes[volume]
        _encryption: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, volume, 3)
            if "Encrypted" in graph.nodes[node]["labels"]
        ]
        if not _encryption:
            continue
        encryption: int = _encryption[0]
        with contextlib.suppress(CloudFormationInvalidTypeError):
            un_encryption: List[int] = get_ref_nodes(
                graph,
                encryption,
                lambda x: x in (False, "false", "False", "0", 0),
            )
            if un_encryption:
                vulnerabilities.append(
                    Vulnerability(
                        path=template["path"],
                        entity="AWS::EC2::Volume",
                        identifier=resource["name"],
                        line=graph.nodes[un_encryption[0]]["line"],
                        reason="is not encrypted",
                    )
                )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 volumes are not encrypted",
        msg_closed="EC2 volumes are encrypted",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_an_iam_instance_profile(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Verify if ``EC2::Instance`` uses an IamInstanceProfile.

    EC2 instances need credentials to access other AWS services.

    An IAM role attached to the instance provides these credentials in a secure
    way. With this, you don't have to manage credentials because they are
    temporarily provided by the IAM Role and are rotated automatically.

    See: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide
    /iam-roles-for-amazon-ec2.html

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not attached an
                IamInstanceProfile.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    vulnerabilities: List[Vulnerability] = []
    instances: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(
            graph.nodes[node]["labels"].intersection(
                {"AWS", "EC2", "Instance"}
            )
        )
        > 2
    ]
    for instance in instances:
        instance_node: Dict = graph.nodes[instance]
        profile: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, instance, 3)
            if "IamInstanceProfile" in graph.nodes[node]["labels"]
        ]
        if not profile:
            template: Dict = graph.nodes[
                get_predecessor(graph, instance, "CloudFormationTemplate")
            ]
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity="AWS::EC2::Instance/IamInstanceProfile",
                    identifier=instance_node["name"],
                    line=instance_node["line"],
                    reason="is not present",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 instances have not an IamInstanceProfile set",
        msg_closed="EC2 instances have an IamInstanceProfile set",
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Verify if ``EC2`` has not deletion protection enabled.

    By default EC2 Instances can be terminated using the Amazon EC2 console,
    CLI, or API.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not the **DisableApiTermination**
                parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    launch_templates: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(
            graph.nodes[node]["labels"].intersection(
                {"AWS", "EC2", "LaunchTemplate", "Instance"}
            )
        )
        > 2
    ]
    for l_template in launch_templates:
        _type = get_type(graph, l_template, {"LaunchTemplate", "Instance"})
        template = graph.nodes[
            get_predecessor(graph, l_template, "CloudFormationTemplate")
        ]
        vulnerable = True
        resource = graph.nodes[l_template]
        line = resource["line"]
        termination = [
            node
            for node in dfs_preorder_nodes(graph, l_template, 15)
            if "DisableApiTermination" in graph.nodes[node]["labels"]
        ]
        if termination:
            termination_node = get_ref_nodes(
                graph,
                termination[0],
                lambda x: x in (False, "false", "False", "0", 0),
            )
            if termination_node:
                line = graph.nodes[termination_node[0]]["line"]
            else:
                vulnerable = False
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=f"AWS::EC2::{_type}/DisableApiTermination/",
                    identifier=resource["name"],
                    line=line,
                    reason="has not disabled api termination",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="EC2 Launch Templates have API termination enabled",
        msg_closed="EC2 Launch Templates have API termination disabled",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def security_group_allows_anyone_to_admin_ports(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if ``EC2::SecurityGroup`` allows connection from internet
    to admin services.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,  # CIFS
    }
    vulnerabilities: list = []

    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)

    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        cidrs: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, group, 10)
            if graph.nodes[node]["labels"].intersection({"CidrIp", "CidrIpv6"})
        ]

        for cidr in cidrs:
            cidr_node = get_ref_nodes(graph, cidr, helper.is_cidr)
            if not cidr_node:
                continue
            is_public_cidr = graph.nodes[cidr_node[0]]["value"] in (
                "::/0",
                "0.0.0.0/0",
            )
            if not is_public_cidr:
                continue

            father = list(graph.predecessors(cidr))[0]
            from_port_node: Union[List[int], int] = nx.utils.flatten(
                [
                    get_ref_nodes(
                        graph, node, lambda y: isinstance(y, (int, float))
                    )
                    for node in dfs_preorder_nodes(graph, father, 1)
                    if "FromPort" in graph.nodes[node]["labels"]
                ]
            )

            to_port_node: Union[List[int], int] = nx.utils.flatten(
                [
                    get_ref_nodes(
                        graph, node, lambda y: isinstance(y, (int, float))
                    )
                    for node in dfs_preorder_nodes(graph, father, 1)
                    if "ToPort" in graph.nodes[node]["labels"]
                ]
            )

            if not from_port_node or not to_port_node:
                continue

            from_port_node = from_port_node[0]
            to_port_node = to_port_node[0]

            _type: str = get_type(
                graph, get_predecessor(graph, cidr, allow_groups), allow_groups
            )
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            from_port: float
            to_port: float
            from_port, to_port = tuple(
                map(
                    float,
                    (
                        graph.nodes[from_port_node]["value"],
                        graph.nodes[to_port_node]["value"],
                    ),
                )
            )

            entities = []
            for port in admin_ports:
                if from_port <= port <= to_port:
                    entities.append(f'{resource["name"]}/{port}')

            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"{resource_type}/{entity}",
                    identifier=resource["name"],
                    line=graph.nodes[from_port_node]["line"],
                    reason="Grants access to admin ports from internet",
                )
                for entity in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=(
            "EC2 security groups have ingress/egress rules "
            "that allow access to admin ports over the internet"
        ),
        msg_closed=(
            "EC2 security groups have ingress/egress rules "
            "that deny access to admin ports over the internet"
        ),
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_dns_access(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if inbound rules that allow unrestricted access to port 53.

    TCP/UDP port 53 is used by the Domain Name Service during DNS resolution.
    Restrict access to TCP and UDP port 53 only those IP addresses that
    require, to implement the principle of least privilege and reduce the
    possibility of a attack.

    Allowing unrestricted  to DNS access can give chance of an attack such as
    Denial of Services (DOS) or Distributed Denial of Service Syn Flood (DDoS).

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)

    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        for rule in _iterate_security_group_rules(graph, group):
            cidr = rule.get("CidrIp", None) or rule.get("CidrIpv6", None)
            is_public_cidr = graph.nodes[cidr]["value"] in (
                "::/0",
                "0.0.0.0/0",
            )
            if not is_public_cidr:
                continue
            entities = []
            from_port, to_port = tuple(
                map(
                    float,
                    (
                        graph.nodes[rule["FromPort"]]["value"],
                        graph.nodes[rule["ToPort"]]["value"],
                    ),
                )
            )
            if from_port <= 53 <= to_port:
                entities.append(f"rule/port/53")
            _type = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"{resource_type}/{entity}",
                    identifier=resource["name"],
                    line=graph.nodes[rule["FromPort"]]["line"],
                    reason=(
                        "Group must restrict access to TCP port"
                        " and UDP 53 to the necessary IP addresses."
                    ),
                )
                for entity in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Security groups allow access to DNS without restrictions.",
        msg_closed=(
            "Security groups allow access to DNS to"
            " the necessary IP addresses."
        ),
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ftp_access(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if security groups allow unrestricted access to TCP ports 20 and 21.

    Restrict access to TCP ports 20 y 21 to only IP addresses that require,
    it in order to implement the principle of least privilege.
    TCP ports 20 and 21 are used for data transfer and communication by the
    File Transfer Protocol (FTP) client-server applications:

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)

    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        for rule in _iterate_security_group_rules(graph, group):
            cidr = rule.get("CidrIp", None) or rule.get("CidrIpv6", None)
            is_public_cidr = graph.nodes[cidr]["value"] in (
                "::/0",
                "0.0.0.0/0",
            )
            if not is_public_cidr:
                continue
            entities = []
            from_port, to_port = tuple(
                map(
                    float,
                    (
                        graph.nodes[rule["FromPort"]]["value"],
                        graph.nodes[rule["ToPort"]]["value"],
                    ),
                )
            )
            _type = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            for port in range(20, 22):
                if from_port <= port <= to_port and str(
                    graph.nodes[rule["IpProtocol"]]["value"]
                ) in ("tcp", "-1"):
                    entities.append(f"rule/port/{port}")

            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"{resource_type}/{entity}",
                    identifier=resource["name"],
                    line=graph.nodes[rule["FromPort"]]["line"],
                    reason=(
                        "Group must restrict access to TCP port"
                        " 20/21 to the necessary IP addresses."
                    ),
                )
                for entity in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Security groups allow access to FTP without restrictions.",
        msg_closed=(
            "Security groups allow access to FTP to"
            " the necessary IP addresses."
        ),
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_security_groups_ip_ranges_in_rfc1918(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if inbound rules access from IP address ranges specified in RFC-1918.

    Using RFC-1918 CIDRs within your EC2 security groups allow an entire
    private network to access EC2 instancess. Restrict access to only those
    private IP addresses that require, it in order to implement the principle
    of least privilege.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    rfc1918 = {
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
    }

    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)

    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        for rule in _iterate_security_group_rules(graph, group):
            cidr = rule.get("CidrIp", None)
            if not cidr:
                continue
            entities = []
            if (
                graph.nodes[cidr]["value"] in rfc1918
                and rule["type"] == "SecurityGroupIngress"
            ):
                entities.append(f"rule/CidrIp/{graph.nodes[cidr]['value']}")
            _type = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"{resource_type}/{entity}",
                    identifier=resource["name"],
                    line=graph.nodes[cidr]["line"],
                    reason=(
                        "Group must restrict access only to the"
                        " necessary private IP addresses."
                    ),
                )
                for entity in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Security groups contain RFC-1918 CIDRs open.",
        msg_closed="Security groups do not contain RFC-1918 CIDRs open.",
    )


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_open_all_ports_to_the_public(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if security groups has all ports or protocols open to the public..

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    allow_groups: Set[str] = {"SecurityGroupEgress", "SecurityGroupIngress"}
    security_groups: List[int] = _get_securitygroups(graph, path, exclude)

    for group in security_groups:
        resource: Dict = graph.nodes[group]
        template = graph.nodes[
            get_predecessor(graph, group, "CloudFormationTemplate")
        ]
        for rule in _iterate_security_group_rules(graph, group):
            cidr = rule.get("CidrIp", None) or rule.get("CidrIpv6", None)
            is_public_cidr = graph.nodes[cidr]["value"] in (
                "::/0",
                "0.0.0.0/0",
            )
            if not is_public_cidr:
                continue
            entities = []
            from_port, to_port = tuple(
                map(
                    float,
                    (
                        graph.nodes[rule["FromPort"]]["value"],
                        graph.nodes[rule["ToPort"]]["value"],
                    ),
                )
            )
            _type = rule["type"]
            resource_type: str = [
                res
                for res in resource["labels"]
                if res in {"SecurityGroup", *allow_groups}
            ][-1]
            resource_type = (
                f"{resource_type}/{_type}"
                if _type != resource_type
                else f"{resource_type}"
            )
            if from_port == 1 and to_port == 65535:
                entities.append(f"{from_port}->{to_port}")
            vulnerabilities.extend(
                Vulnerability(
                    path=template["path"],
                    entity=f"{resource_type}/FromPort->ToPort/{entity}",
                    identifier=resource["name"],
                    line=graph.nodes[rule["FromPort"]]["line"],
                    reason="Grants public access to all ports",
                )
                for entity in entities
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Security groups has all ports open to the pubic",
        msg_closed="Security groups do not have all ports open to the pubic.",
    )
