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
    EventName,
    Trigger,
)

TRIGGERS: tuple[Trigger, ...] = (
    Trigger(
        batch_size=20,
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.event_name == EventName.INSERT
        ),
        records_processor=webhooks.process,
    ),
    Trigger(
        batch_size=0,
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=opensearch.process_vulns,
    ),
    Trigger(
        batch_size=0,
        records_filter=(
            lambda record: record.pk.startswith("FIN#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_findings,
    ),
    Trigger(
        batch_size=0,
        records_filter=(
            lambda record: record.pk.startswith("EXEC#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_executions,
    ),
    Trigger(
        batch_size=0,
        records_filter=(
            lambda record: record.event_name == EventName.REMOVE
            and record.pk.startswith("FIN#")
        ),
        records_processor=redshift.process_findings,
    ),
    Trigger(
        batch_size=0,
        records_filter=(
            lambda record: record.pk.startswith("EVENT#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_events,
    ),
)
