"""AWS cloud checks for ``FSx```."""


from typing import List, Tuple, Dict

# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import MEDIUM
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> Tuple:
    """Check if an ``FSx Filesystem`` uses default KMS key.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    filesystems: List[Dict] = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='fsx',
        func='describe_file_systems',
        param='FileSystems',
        retry=retry)

    kms_aliases: List[Dict] = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='kms',
        func='list_aliases',
        param='Aliases',
        retry=retry)

    msg_open: str = 'FSx FileSystems encrypted with default KMS key'
    msg_closed: str = 'FSx FileSystems not encrypted with default KMS key'

    vulns: List = []
    safes: List = []
    for filesystem in filesystems:
        vol_key = filesystem.get('KmsKeyId', '')
        if vol_key:
            for alias in kms_aliases:
                (vulns if alias.get('TargetKeyId', '') == vol_key.split("/")[1]
                 and alias.get('AliasName') == "alias/aws/fsx"
                 else safes).append(
                     (filesystem['FileSystemId'],
                      'uses default KMS key'))

    return _get_result_as_tuple(
        service='FSx',
        objects='FileSystems',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
