import boto3
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
import os
from typing import (
    Any,
)

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
INDEX = "vulnerabilities"


def handle(event: dict[str, Any], _context: Any) -> None:
    for record in event["Records"]:
        pk: str = record["dynamodb"]["Keys"]["pk"]["S"]
        sk: str = record["dynamodb"]["Keys"]["sk"]["S"]
        item_id = "#".join([pk, sk])

        if record["eventName"] == "REMOVE":
            CLIENT.delete(id=item_id, index=INDEX)
        else:
            item = record["dynamodb"]["NewImage"]
            CLIENT.index(body=item, id=item_id, index=INDEX)
