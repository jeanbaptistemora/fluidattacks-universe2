from dynamodb.context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_ENVIRONMENT,
)
from dynamodb.utils import (
    deserialize_dynamodb_json,
    SESSION,
)
from opensearchpy import (
    AWSV4SignerAuth,
    NotFoundError,
    OpenSearch,
    RequestsHttpConnection,
)
from typing import (
    Any,
    Optional,
)

CREDENTIALS = SESSION.get_credentials()
CLIENT = OpenSearch(
    connection_class=RequestsHttpConnection,
    hosts=[FI_AWS_OPENSEARCH_HOST],
    http_auth=AWSV4SignerAuth(CREDENTIALS, SESSION.region_name),
    http_compress=True,
    use_ssl=FI_ENVIRONMENT == "prod",
    verify_certs=FI_ENVIRONMENT == "prod",
)


def _replicate_on_opensearch(
    event_name: str,
    pk: str,
    sk: str,
    item: Optional[dict[str, Any]],
) -> None:
    """Replicates the item on AWS OpenSearch"""
    matches_filters = pk.startswith("VULN#") and sk.startswith("FIN#")

    if matches_filters:
        item_id = "#".join([pk, sk])

        if event_name == "REMOVE":
            try:
                CLIENT.delete(id=item_id, index="vulnerabilities")
            except NotFoundError:
                print("Item", pk, sk, "not found. Won't delete")
        else:
            CLIENT.index(body=item, id=item_id, index="vulnerabilities")


def replicate(records: tuple[dict[str, Any], ...]) -> None:
    """Replicates the records on other storages"""
    for record in records:
        event_name: str = record["eventName"]
        pk: str = record["dynamodb"]["Keys"]["pk"]["S"]
        sk: str = record["dynamodb"]["Keys"]["sk"]["S"]
        item = (
            deserialize_dynamodb_json(record["dynamodb"]["NewImage"])
            if "NewImage" in record["dynamodb"]
            else None
        )

        if FI_ENVIRONMENT != "prod":
            print("Processing", event_name, pk, sk)

        _replicate_on_opensearch(event_name, pk, sk, item)
