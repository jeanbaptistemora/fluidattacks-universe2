"""AWS cloud checks for ``EFS```."""


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


def _get_filesystems(key_id, retry, secret, session_token):
    pools = []
    data = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='efs',
        func='describe_file_systems',
        boto3_client_kwargs={'aws_session_token': session_token},
        MaxItems=50,
        retry=retry)
    pools += data.get('FileSystems', [])
    next_token = data.get('Marker', '')
    while next_token:
        data = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='efs',
            func='describe_file_systems',
            boto3_client_kwargs={'aws_session_token': session_token},
            MaxItems=50,
            Marker=next_token,
            retry=retry)
        pools += data['FileSystems']
        next_token = data.get('NextMarker', '')
    return pools


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """Check if an ``EFS filesystem`` uses default KMS key.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    filesystems = _get_filesystems(key_id, retry, secret, session_token)

    kms_aliases = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='kms',
        func='list_aliases',
        param='Aliases',
        retry=retry)

    msg_open: str = 'EFS filesystems encrypted with default KMS key'
    msg_closed: str = 'EFS filesystems not encrypted with default KMS key'

    vulns, safes = [], []
    for filesystem in filesystems:
        vol_key = filesystem.get('KmsKeyId', '')
        if vol_key:
            for alias in kms_aliases:
                (vulns if alias.get('TargetKeyId', '') == vol_key.split("/")[1]
                 and alias.get('AliasName') == "alias/aws/elasticfilesystem"
                 else safes).append(
                     (filesystem['FileSystemId'],
                      'uses default KMS key'))

    return _get_result_as_tuple(
        service='EFS',
        objects='Filesystems',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_encryption_disabled(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """Check if an ``EFS filesystem`` has encryption disabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    filesystems = _get_filesystems(key_id, retry, secret, session_token)

    msg_open: str = 'EFS filesystems have encryption disabled'
    msg_closed: str = 'EFS filesystems have encryption enabled'

    vulns, safes = [], []
    for filesystem in filesystems:
        (vulns if not filesystem.get('Encrypted')
         else safes).append(
             (filesystem['FileSystemId'],
              'has encryption disabled'))

    return _get_result_as_tuple(
        service='EFS',
        objects='Filesystems',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
