"""AWS cloud checks (VPC)."""

# standard imports
import json
from typing import List

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM, LOW
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
        egress_rules = list(
            filter(lambda x: egress == x['Egress'], rule['Entries']))
        if egress_rules and _acl_rule_is_public(egress_rules[0], egress,
                                                action):
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
    msg_open: str = 'Network ACLs allow all ingress traffic for all ports.'
    msg_closed: str = \
        'Network ACLs do not allow all ingress traffic for all ports.'
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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def network_acls_allow_all_egress_traffic(key_id: str,
                                          secret: str,
                                          retry: bool = True) -> tuple:
    """
    Check if network ACLs allow all egress traffic for all ports.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are network ACLs that allow all
                egress traffic.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network ACLs allow all egress traffic for all ports.'
    msg_closed: str = \
        'Network ACLs do not allow all egress traffic for all ports.'
    vulns, safes = [], []

    network_acls = aws.run_boto3_func(key_id=key_id,
                                      secret=secret,
                                      service='ec2',
                                      func='describe_network_acls',
                                      param='NetworkAcls',
                                      retry=retry)

    vuln_ids = _network_acls_allow_all_traffic(
        network_acls, 'egress', 'allow')
    safe_ids = set(
        map(lambda x: x['NetworkAclId'], network_acls)) - set(vuln_ids)
    message = 'do not allow all egress traffic for all ports.'
    safes = [(i, message) for i in safe_ids]
    vulns = [(i, message) for i in vuln_ids]

    return _get_result_as_tuple(
        service='VPC',
        objects='Network ACLs',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def vpc_endpoints_exposed(key_id: str, secret: str,
                          retry: bool = True) -> tuple:
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
    msg_open: str = 'VPC endpoints are accessible by any IAM user or service.'
    msg_closed: str = \
        'VPC endpoints are not accessible to any IAM user or service.'
    vulns, safes = [], []
    vpc_endpoints = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_vpc_endpoints',
        param='VpcEndpoints',
        retry=retry)
    for endpoint in vpc_endpoints:
        if endpoint['VpcEndpointType'] != 'Interface':
            policy_document = json.loads(endpoint['PolicyDocument'])
            vulnerable = [
                sts['Principal'] in ['*', {
                    'AWS': '*'
                }] and 'Condition' not in sts.keys()
                for sts in policy_document['Statement']
            ]
            (vulns if any(vulnerable) else safes).append(
                (vpc_endpoints[0]['VpcEndpointId'],
                 'do not allow access to any IAM user or service.'))

    return _get_result_as_tuple(
        service='VPC',
        objects='Endpoints',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def vpc_flow_logs_disabled(key_id: str, secret: str,
                           retry: bool = True) -> tuple:
    """
    Check if the VPCs has flow logs disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are VPC whit flow logs disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'VPCs has flow logs disabled.'
    msg_closed: str = 'VPCs has flow logs enabled.'
    vulns, safes = [], []
    vpcs = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_vpcs',
        param='Vpcs',
        retry=retry)
    for vpc in vpcs:
        filters = [{'Name': 'resource-id', 'Values': [vpc['VpcId']]}]
        flow_logs = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ec2',
            func='describe_flow_logs',
            param='FlowLogs',
            retry=retry,
            Filters=filters)
        (vulns if not flow_logs else safes).append(
            (vpc['VpcId'], 'must enable flow logs.'))

    return _get_result_as_tuple(
        service='VPC',
        objects='VPCs',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
