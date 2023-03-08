"""AWS cloud checks (VPC)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    LOW,
    MEDIUM,
)
from fluidasserts.cloud.aws import (
    _get_result_as_tuple,
)
from fluidasserts.helper import (
    aws,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
import json
from typing import (
    List,
)


def _acl_rule_is_public(acl_rule: dict, egress: bool, action: str) -> bool:
    """Check if an ACL rule allow all ingress traffic."""
    is_public = False
    if acl_rule["Egress"] == egress and acl_rule["RuleAction"] == action:
        if "CidrBlock" in acl_rule.keys():
            is_public = acl_rule["CidrBlock"] == "0.0.0.0/0"
        if "Ipv6CidrBlock" in acl_rule.keys():
            is_public = acl_rule["Ipv6CidrBlock"] == "::/0"
    return (
        is_public
        and "PortRange" not in acl_rule.keys()
        and acl_rule["Protocol"] == "-1"
    )


def _network_acls_allow_all_traffic(
    network_acls: dict, direction: str, action: str
) -> List[str]:
    """
    Check if the network ACLs allow all traffic.

    :param network_acls: Network ACLs.
    :param direction: direction of traffic (ingress | egress).
    :param action: action of rules (allow | deny).

    :returns: A list with the IDs of network ACLs that comply the condition.
    """
    egress = bool(direction == "egress")
    success = []
    for rule in network_acls:
        egress_rules = list(
            filter(lambda x: egress == x["Egress"], rule["Entries"])
        )
        if egress_rules and _acl_rule_is_public(
            egress_rules[0], egress, action
        ):
            success.append(rule["NetworkAclId"])
    return success


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def vpc_endpoints_exposed(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if any user or IAM service can access the VPC endpoint.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are VPC endpoints accessible by any IAM
                user or service.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "VPC endpoints are accessible by any IAM user or service."
    msg_closed: str = (
        "VPC endpoints are not accessible to any IAM user or service."
    )
    vulns, safes = [], []
    vpc_endpoints = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_vpc_endpoints",
        param="VpcEndpoints",
        retry=retry,
    )
    for endpoint in vpc_endpoints:
        if endpoint["VpcEndpointType"] != "Interface":
            policy_document = json.loads(endpoint["PolicyDocument"])
            vulnerable = [
                sts["Principal"] in ["*", {"AWS": "*"}]
                and "Condition" not in sts.keys()
                for sts in policy_document["Statement"]
            ]
            (vulns if any(vulnerable) else safes).append(
                (
                    vpc_endpoints[0]["VpcEndpointId"],
                    "do not allow access to any IAM user or service.",
                )
            )

    return _get_result_as_tuple(
        service="VPC",
        objects="Endpoints",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
