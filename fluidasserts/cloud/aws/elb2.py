"""AWS cloud checks for ``ELB v2``` (Elastic Load Balancing version 2)."""

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts import DAST, LOW
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_access_logging_disabled(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check if ``LoadBalancers`` have **access_logs.s3.enabled** set to **true**.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    balancers = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='elbv2',
                                   func='describe_load_balancers',
                                   param='LoadBalancers',
                                   retry=retry)

    msg_open: str = 'ELB Load Balancers have access logging disabled'
    msg_closed: str = 'ELB Load Balancers have access logging enabled'

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for attrs in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    service='elbv2',
                    func='describe_load_balancer_attributes',
                    param='Attributes',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):

                if attrs['Key'] == 'access_logs.s3.enabled':
                    (vulns if attrs['Value'] != 'true' else safes).append(
                        (load_balancer_arn,
                         'access_logs.s3.enabled must be enabled'))

    return _get_result_as_tuple(
        service='ELBv2', objects='Load Balancers version 2',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_deletion_protection(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check if ``LoadBalancers`` have **Deletion Protection**.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    balancers = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='elbv2',
                                   func='describe_load_balancers',
                                   param='LoadBalancers',
                                   retry=retry)

    msg_open: str = 'ELB Load Balancers have not deletion protection'
    msg_closed: str = 'ELB Load Balancers clusters have deletion protection'

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for attrs in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    service='elbv2',
                    func='describe_load_balancer_attributes',
                    param='Attributes',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):

                if attrs['Key'] == 'deletion_protection.enabled':
                    (vulns if attrs['Value'] != 'true' else safes).append(
                        (load_balancer_arn,
                         'deletion_protection.enabled must be enabled'))

    return _get_result_as_tuple(
        service='ELBv2', objects='Load Balancers version 2',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
