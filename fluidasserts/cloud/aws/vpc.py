"""AWS cloud checks (VPC)."""

# standard imports
from typing import List

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _acl_rule_is_public(acl_rule: dict, egress: bool, action: str) -> bool:
    """Check if an ACL rule allow all ingress traffic."""
    is_public = False
    if acl_rule['Egress'] == egress and acl_rule['RuleAction'] == action:
        if 'CidrBlock' in acl_rule.keys():
            is_public = acl_rule['CidrBlock'] == '0.0.0.0/0'
        if 'Ipv6CidrBlock' in acl_rule.keys():
            is_public = acl_rule['Ipv6CidrBlock'] == '::/0'
    return is_public and 'PortRange' not in acl_rule.keys(
    ) and acl_rule['Protocol'] == '-1'


def _network_acls_allow_all_traffic(network_acls: dict, direction: str,
                                    action: str) -> List[str]:
    """
    Check if the network ACLs allow all traffic.

    :param network_acls: Network ACLs.
    :param direction: direction of traffic (ingress | egress).
    :param action: action of rules (allow | deny).

    :returns: A list with the IDs of network ACLs that comply the condition.
    """
    egress = bool(direction == 'egress')
    success = []
    for rule in network_acls:
        egress = list(filter(lambda x: egress == x['Egress'], rule['Entries']))
        if egress and _acl_rule_is_public(egress[0], False, action):
            success.append(rule['NetworkAclId'])
    return success


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def network_acls_allow_all_ingress_traffic(key_id: str,
                                           secret: str,
                                           retry: bool = True) -> tuple:
    """
    Check if network ACLs allow all ingress traffic for all ports.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are network ACLs that allow all
                ingress traffic.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network ACLs allow all ingress traffic foll al ports.'
    msg_closed: str = \
        'Network ACLs do not allow all ingress traffic foll al ports.'
    vulns, safes = [], []

    network_acls = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_network_acls',
        param='NetworkAcls',
        retry=retry)

    vuln_ids = _network_acls_allow_all_traffic(network_acls, 'ingress',
                                               'allow')
    safe_ids = set(map(lambda x: x['NetworkAclId'],
                       network_acls)) - set(vuln_ids)
    message = 'do not allow all ingress traffic for all ports.'
    safes = [(i, message) for i in safe_ids]
    vulns = [(i, message) for i in vuln_ids]

    return _get_result_as_tuple(
        service='VPC',
        objects='Network ACLs',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
