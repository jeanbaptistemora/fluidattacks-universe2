"""AWS cloud checks for ``ELB v2``` (Elastic Load Balancing version 2)."""

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts import DAST, LOW, HIGH, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_access_logging_disabled(key_id: str,
                                secret: str,
                                session_token: str = None,
                                retry: bool = True) -> tuple:
    """
    Check if ``LoadBalancers`` have **access_logs.s3.enabled** set to **true**.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
                    boto3_client_kwargs={'aws_session_token': session_token},
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
        service='ELBv2',
        objects='Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_deletion_protection(key_id: str,
                                secret: str,
                                session_token: str = None,
                                retry: bool = True) -> tuple:
    """
    Check if ``LoadBalancers`` have **Deletion Protection**.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
                    boto3_client_kwargs={'aws_session_token': session_token},
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
        service='ELBv2',
        objects='Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def listeners_not_using_https(key_id: str,
                              secret: str,
                              session_token: str = None,
                              retry: bool = True) -> tuple:
    """
    Check if Listeners use HTTPS**.

    https://www.cloudconformity.com/knowledge-base/aws/ELB/
    app-tier-elb-https-listener.html

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_load_balancers',
        param='LoadBalancers',
        retry=retry)

    msg_open: str = 'ELB Load Balancers dont use HTTPS'
    msg_closed: str = 'ELB Load Balancers use HTTPS'

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for listener in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    boto3_client_kwargs={'aws_session_token': session_token},
                    service='elbv2',
                    func='describe_listeners',
                    param='Listeners',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):

                (vulns if listener['Protocol'] == 'HTTP'
                 else safes).append(
                     (load_balancer_arn,
                      'protocol must be HTTPS'))

    return _get_result_as_tuple(
        service='ELBv2',
        objects='Application Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_insecure_ssl_protocol(key_id: str,
                               secret: str,
                               session_token: str = None,
                               retry: bool = True) -> tuple:
    """
    Check if Listeners uses unsafe SSL protocol.

    https://www.cloudconformity.com/knowledge-base/aws/ELB/
    elb-insecure-ssl-protocols.html#

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    acceptable = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_ssl_policies',
        param='SslPolicies',
        Names=['ELBSecurityPolicy-2016-08'],
        retry=retry)

    acceptable_protos = acceptable.get('SslProtocols', [])

    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_load_balancers',
        param='LoadBalancers',
        retry=retry)

    msg_open: str = 'ELB Load Balancers allow insecure SSL protocols'
    msg_closed: str = 'ELB Load Balancers do not allow insecure SSL protocols'

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for listener in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    boto3_client_kwargs={'aws_session_token': session_token},
                    service='elbv2',
                    func='describe_listeners',
                    param='Listeners',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):
                if listener.get('SslPolicy', ''):
                    policy = aws.run_boto3_func(
                        key_id=key_id,
                        secret=secret,
                        boto3_client_kwargs={
                            'aws_session_token': session_token},
                        service='elbv2',
                        func='describe_ssl_policies',
                        param='Listeners',
                        Names=[listener['SslPolicy']],
                        retry=retry)

                    for protocol in policy['SslProtocols']:
                        (vulns if protocol not in acceptable_protos
                         else safes).append(
                             (f'{listener["LoadBalancerArn"]}/{protocol}',
                              'protocol is unsafe'))

    return _get_result_as_tuple(
        service='ELBv2',
        objects='Application Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_insecure_ssl_cipher(key_id: str,
                             secret: str,
                             session_token: str = None,
                             retry: bool = True) -> tuple:
    """
    Check if Listeners uses unsafe SSL cipher.

    https://www.cloudconformity.com/knowledge-base/aws/ELB/
    elb-insecure-ssl-ciphers.html#

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    acceptable = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_ssl_policies',
        param='SslPolicies',
        Names=['ELBSecurityPolicy-2016-08'],
        retry=retry)

    acceptable_protos = acceptable.get('Ciphers', [])

    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_load_balancers',
        param='LoadBalancers',
        retry=retry)

    msg_open: str = 'ELB Load Balancers allows insecure SSL ciphers'
    msg_closed: str = 'ELB Load Balancers does not allow insecure SSL ciphers'

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for listener in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    boto3_client_kwargs={'aws_session_token': session_token},
                    service='elbv2',
                    func='describe_listeners',
                    param='Listeners',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):
                if listener.get('SslPolicy', ''):
                    policy = aws.run_boto3_func(
                        key_id=key_id,
                        secret=secret,
                        boto3_client_kwargs={
                            'aws_session_token': session_token},
                        service='elbv2',
                        func='describe_ssl_policies',
                        param='Listeners',
                        Names=[listener['SslPolicy']],
                        retry=retry)

                    for cipher in policy['Ciphers']:
                        (vulns if cipher not in acceptable_protos
                         else safes).append(
                             (f'{listener["LoadBalancerArn"]}/'
                              f'{cipher["Name"]}',
                              'cipher is unsafe'))

    return _get_result_as_tuple(
        service='ELBv2',
        objects='Application Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_insecure_security_policy(key_id: str,
                                  secret: str,
                                  session_token: str = None,
                                  retry: bool = True) -> tuple:
    """
    Check if Listeners uses unsafe security policy.

    https://www.cloudconformity.com/knowledge-base/aws/ELBv2/
    network-load-balancer-security-policy.html#

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    acceptable = ('ELBSecurityPolicy-2016-08',
                  'ELBSecurityPolicy-TLS-1-1-2017-01',
                  'ELBSecurityPolicy-FS-2018-06',
                  'ELBSecurityPolicy-TLS-1-2-Ext-2018-06')

    balancers = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elbv2',
        func='describe_load_balancers',
        param='LoadBalancers',
        retry=retry)

    msg_open: str = 'ELB Load Balancers implement insecure security policy'
    msg_closed: str = ('ELB Load Balancers does not implement '
                       'insecure security policy')

    vulns, safes = [], []

    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer['LoadBalancerArn']

            for listener in aws.run_boto3_func(
                    key_id=key_id,
                    secret=secret,
                    boto3_client_kwargs={'aws_session_token': session_token},
                    service='elbv2',
                    func='describe_listeners',
                    param='Listeners',
                    LoadBalancerArn=load_balancer_arn,
                    retry=retry):
                if listener.get('SslPolicy', ''):
                    (vulns if listener.get('SslPolicy', '') not in acceptable
                     else safes).append(
                         (f'{listener["LoadBalancerArn"]}/'
                          f'{listener["SslPolicy"]}',
                          'security policy is unsafe'))

    return _get_result_as_tuple(
        service='ELBv2',
        objects='Application Load Balancers version 2',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
