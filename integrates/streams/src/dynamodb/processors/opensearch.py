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
        bulk(client=CLIENT, actions=actions)
    except BulkIndexError as ex:
        LOGGER.exception(ex, extra={"extra": {"errors": ex.errors}})


def process_vulns(records: tuple[Record, ...]) -> None:
    _process(records, "vulnerabilities")


def process_findings(records: tuple[Record, ...]) -> None:
    _process(records, "findings")


def process_executions(records: tuple[Record, ...]) -> None:
    _process(records, "forces_executions")


def process_events(records: tuple[Record, ...]) -> None:
    _process(records, "events")


def process_lines(records: tuple[Record, ...]) -> None:
    _process(records, "toe_lines")
