# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from dynamodb.context import (
    FI_ENVIRONMENT,
)
from dynamodb.processors import (
    opensearch,
    redshift,
    webhooks,
)
from dynamodb.types import (
    StreamEvent,
    Trigger,
)

TRIGGERS: tuple[Trigger, ...] = (
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.event_name == StreamEvent.INSERT
        ),
        records_processor=webhooks.process_google_chat,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=webhooks.process_poc,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("EVENT#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_events,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("EXEC#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_executions,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("FIN#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_findings,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=opensearch.process_vulns,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.event_name == StreamEvent.REMOVE
        ),
        records_processor=redshift.process_records,
    ),
)
