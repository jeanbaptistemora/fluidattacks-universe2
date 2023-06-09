from dynamodb.context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_ENVIRONMENT,
)
from dynamodb.resource import (
    SESSION,
)
from dynamodb.types import (
    Record,
    StreamEvent,
)
from dynamodb.utils import (
    SetEncoder,
)
import logging
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
from opensearchpy.helpers import (
    bulk,
    BulkIndexError,
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
    max_retries=10,
    retry_on_status=(429, 502, 503, 504),
    retry_on_timeout=True,
    serializer=SetEncoder(),
    use_ssl=FI_ENVIRONMENT == "prod",
    verify_certs=FI_ENVIRONMENT == "prod",
)
LOGGER = logging.getLogger(__name__)


def _process(records: tuple[Record, ...], index: str) -> None:
    """Replicates the item on AWS OpenSearch"""
    actions: list[dict[str, Any]] = []

    for record in records:
        action_name = (
            "delete" if record.event_name == StreamEvent.REMOVE else "index"
        )
        action = {
            "_id": "#".join([record.pk, record.sk]),
            "_index": index,
            "_op_type": action_name,
        }
        if action_name == "index" and record.new_image:
            actions.append({**action, "_source": record.new_image})
        else:
            actions.append(action)

    try:
        bulk(client=CLIENT, actions=actions, ignore_status=(404,))
    except BulkIndexError as ex:
        LOGGER.exception(ex, extra={"extra": {"errors": ex.errors}})


def _format_vulns(records: tuple[Record, ...]) -> tuple[Record, ...]:
    formatted = []

    for record in records:
        if (
            record.event_name in {StreamEvent.INSERT, StreamEvent.MODIFY}
            and record.new_image
            and "hash" in record.new_image
        ):
            # Needed as it doesn't fit in OpenSearch long data type (2^63)
            record.new_image["hash"] = str(record.new_image["hash"])
        formatted.append(record)
    return tuple(formatted)


def process_vulns(records: tuple[Record, ...]) -> None:
    formatted = _format_vulns(records)
    _process(formatted, "vulnerabilities")


def process_findings(records: tuple[Record, ...]) -> None:
    _process(records, "findings")


def process_executions(records: tuple[Record, ...]) -> None:
    _process(records, "forces_executions")


def process_events(records: tuple[Record, ...]) -> None:
    _process(records, "events")


def process_lines(records: tuple[Record, ...]) -> None:
    _process(records, "toe_lines")
