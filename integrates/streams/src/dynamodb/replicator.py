import boto3
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
import os

FI_AWS_OPENSEARCH_HOST = os.environ["AWS_OPENSEARCH_HOST"]
SESSION = boto3.Session()
CREDENTIALS = SESSION.get_credentials()
CLIENT = OpenSearch(
    connection_class=RequestsHttpConnection,
    hosts=[FI_AWS_OPENSEARCH_HOST],
    http_auth=AWSV4SignerAuth(CREDENTIALS, SESSION.region_name),
    http_compress=True,
    use_ssl=True,
    verify_certs=True,
)


def replicate() -> None:
    pass
