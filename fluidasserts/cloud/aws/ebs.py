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


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_encryption_disabled(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """Check if an ``EBS volume`` has encryption disabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    volumes = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='ec2',
        func='describe_volumes',
        param='Volumes',
        retry=retry)

    msg_open: str = 'EBS Volumes have encryption disabled'
    msg_closed: str = 'EBS Volumes have encryption enabled'

    vulns, safes = [], []
    for volume in volumes:
        (vulns if not volume.get('Encrypted')
         else safes).append(
             (volume['VolumeId'],
              'has encryption disabled'))

    return _get_result_as_tuple(
        service='EBS',
        objects='EBS Volumes',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
