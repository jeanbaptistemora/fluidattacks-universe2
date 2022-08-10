from dynamodb.context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_ENVIRONMENT,
)
from dynamodb.types import (
    EventName,
    Record,
)
from dynamodb.utils import (
    format_record,
    SESSION,
)
from more_itertools import (
    chunked,
)
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
from typing import (
    Any,
)

CREDENTIALS = SESSION.get_credentials()
CLIENT = OpenSearch(
    connection_class=RequestsHttpConnection,
    hosts=[FI_AWS_OPENSEARCH_HOST],
    http_auth=AWSV4SignerAuth(CREDENTIALS, SESSION.region_name),
    http_compress=True,
    timeout=100,
    use_ssl=FI_ENVIRONMENT == "prod",
    verify_certs=FI_ENVIRONMENT == "prod",
)


def _replicate_on_opensearch(records: tuple[Record, ...]) -> None:
    """Replicates the item on AWS OpenSearch"""

    def _replicate_chunk(chunk: tuple[Record, ...]) -> None:
        body = []

        for record in chunk:
            action_name = (
                "delete" if record.event_name == EventName.REMOVE else "index"
            )
            action = {
                action_name: {
                    "_index": "vulnerabilities",
                    "_id": "#".join([record.pk, record.sk]),
                }
            }
            body.append(action)

            if action_name == "index":
                body.append(record.item)

        CLIENT.bulk(body=body)

    records_to_replicate = tuple(
        record
        for record in records
        if record.pk.startswith("VULN#") and record.sk.startswith("FIN#")
    )
    chunk_size = 100

    for chunk in chunked(records_to_replicate, chunk_size):
        _replicate_chunk(chunk)


def replicate(raw_records: tuple[dict[str, Any], ...]) -> None:
    """Replicates the records on secondary storages"""
    records = tuple(format_record(record) for record in raw_records)

    _replicate_on_opensearch(records)
