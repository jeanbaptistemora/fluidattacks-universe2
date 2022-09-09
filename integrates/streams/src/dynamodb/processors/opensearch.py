# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb.context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_ENVIRONMENT,
)
from dynamodb.resource import (
    SESSION,
)
from dynamodb.types import (
    EventName,
    Record,
)
from dynamodb.utils import (
    SetEncoder,
)
from more_itertools import (
    chunked,
)
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
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
    serializer=SetEncoder(),
)


def _process(records: tuple[Record, ...], index: str) -> None:
    """Replicates the item on AWS OpenSearch"""
    chunk_size = 100

    for chunk in chunked(records, chunk_size):
        body = []

        for record in chunk:
            action_name = (
                "delete" if record.event_name == EventName.REMOVE else "index"
            )
            action = {
                action_name: {
                    "_index": index,
                    "_id": "#".join([record.pk, record.sk]),
                }
            }
            body.append(action)

            if action_name == "index" and record.item:
                body.append(record.item)

        CLIENT.bulk(body=body)


def process_vulns(records: tuple[Record, ...]) -> None:
    _process(records, "vulnerabilities")


def process_findings(records: tuple[Record, ...]) -> None:
    _process(records, "findings")
