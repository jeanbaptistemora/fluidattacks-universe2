"""AWS cloud checks for ``EBS``` (Elastic Block Storage)."""


# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import HIGH
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


def _get_domains(key_id, retry, secret, session_token):
    domains = []
    data = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='route53domains',
        func='list_domains',
        boto3_client_kwargs={'aws_session_token': session_token},
        MaxItems=50,
        retry=retry)
    domains += data.get('Domains', [])
    next_token = data.get('NextPageMarker', '')
    while next_token:
        data = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='route53domains',
            func='list_domains',
            boto3_client_kwargs={'aws_session_token': session_token},
            MaxRecords=50,
            Marker=next_token,
            retry=retry)
        domains += data['Domains']
        next_token = data.get('NextPageMarker', '')
    return domains


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_privacy_protection_disabled(key_id: str,
                                   secret: str,
                                   session_token: str = None,
                                   retry: bool = True) -> tuple:
    """Check if a ``Route53 Domain`` has privacy protection disabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []
    domains = _get_domains(key_id, retry, secret, session_token)

    for domain in domains:
        privacy = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='route53domains',
            func='get_domain_detail',
            param='RegistrantPrivacy',
            DomainName=domain['DomainName'],
            retry=retry)

        (vulns if not privacy
         else safes).append(
             (domain['DomainName'],
              'has privacy protection disabled'))

    msg_open: str = 'Route53 domains have privacy protection disabled'
    msg_closed: str = 'Route53 domains have privacy protection enabled'

    return _get_result_as_tuple(
        service='Route53',
        objects='Domains',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
