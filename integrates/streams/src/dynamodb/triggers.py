from dynamodb.processors import (
    opensearch,
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
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=webhooks.process,
    ),
    Trigger(
        batch_size=100,
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.event_name == EventName.INSERT
        ),
        records_processor=opensearch.process,
    ),
)
