from collections import (
    defaultdict,
)
from dynamodb.processor import (
    replicate_on_opensearch,
    trigger_webhooks,
)
from dynamodb.types import (
    EventName,
    Record,
    Trigger,
)
from dynamodb.utils import (
    format_record,
)
from typing import (
    Any,
)

TRIGGERS: tuple[Trigger, ...] = (
    Trigger(
        batch_size=20,
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=trigger_webhooks,
    ),
    Trigger(
        batch_size=100,
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.event_name == EventName.INSERT
        ),
        records_processor=replicate_on_opensearch,
    ),
)


def trigger_processors(raw_records: tuple[dict[str, Any], ...]) -> None:
    """Triggers the processors according to its preferences"""
    records = (format_record(record) for record in raw_records)
    batches: dict[Trigger, list] = defaultdict(list)

    for trigger in TRIGGERS:
        matching_records = (
            record for record in records if trigger.records_filter(record)
        )
        batches[trigger].extend(matching_records)

        if len(batches[trigger]) >= trigger.batch_size:
            batch: list[Record] = batches[trigger][: trigger.batch_size]
            trigger.records_processor(tuple(batch))
            batches[trigger] = batches[trigger][trigger.batch_size :]
