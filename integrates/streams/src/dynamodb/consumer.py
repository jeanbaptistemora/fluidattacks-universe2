# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from collections import (
    defaultdict,
)
from dynamodb.checkpoint import (
    get_checkpoint,
    remove_checkpoint,
    save_checkpoint,
)
from dynamodb.resource import (
    CLIENT,
    TABLE_NAME,
)
from dynamodb.triggers import (
    TRIGGERS,
)
from dynamodb.types import (
    Record,
    Trigger,
)
from dynamodb.utils import (
    format_record,
)
import logging
import signal
from threading import (
    Event,
    Thread,
)
from time import (
    sleep,
)
from typing import (
    Any,
    Iterator,
    Optional,
)

LOGGER = logging.getLogger(__name__)


def _get_stream_arn(table_name: str) -> str:
    """Returns the ARN of the stream for the requested table"""
    response = CLIENT.list_streams(TableName=table_name)

    return response["Streams"][0]["StreamArn"]


def _describe_stream(
    exclusive_start_shard_id: Optional[str], stream_arn: str
) -> dict[str, Any]:
    """
    Returns information about a stream

    Workaround needed as boto doesn't allow ExclusiveStartShardId to be None
    """
    if exclusive_start_shard_id is None:
        args = {"StreamArn": stream_arn}
    else:
        args = {
            "ExclusiveStartShardId": exclusive_start_shard_id,
            "StreamArn": stream_arn,
        }

    return CLIENT.describe_stream(**args)


def _get_stream_shards(
    stream_arn: str,
) -> Iterator[tuple[dict[str, Any], ...]]:
    """Yields the shards for the requested stream"""
    current_shard_id = None

    while True:
        response = _describe_stream(current_shard_id, stream_arn)
        description = response["StreamDescription"]
        shards = description["Shards"]

        yield shards

        current_shard_id = description.get("LastEvaluatedShardId")

        if current_shard_id is None:
            break


def _get_shard_iterator(stream_arn: str, shard_id: str) -> str:
    """Returns the iterator id for the requested shard"""
    shard_checkpoint = get_checkpoint(shard_id)

    if shard_checkpoint:
        LOGGER.info("%s starting from checkpoint", shard_id)
        response = CLIENT.get_shard_iterator(
            SequenceNumber=shard_checkpoint,
            ShardId=shard_id,
            ShardIteratorType="AFTER_SEQUENCE_NUMBER",
            StreamArn=stream_arn,
        )
    else:
        LOGGER.info("%s starting from the beginning", shard_id)
        response = CLIENT.get_shard_iterator(
            ShardId=shard_id,
            ShardIteratorType="TRIM_HORIZON",
            StreamArn=stream_arn,
        )

    return response["ShardIterator"]


def _get_shard_records(
    shard_id: str,
    shard_iterator: str,
) -> Iterator[tuple[Record, ...]]:
    """Yields the records for the requested iterator"""
    current_iterator = shard_iterator

    while True:
        try:
            response = CLIENT.get_records(ShardIterator=current_iterator)
            records = tuple(
                format_record(record) for record in response["Records"]
            )

            yield records

            current_iterator = response.get("NextShardIterator")

            if current_iterator is None:
                LOGGER.warning("%s closed, moving on", shard_id)
                break
        except CLIENT.exceptions.ExpiredIteratorException:
            LOGGER.warning("%s expired, moving on", shard_iterator)
            break


def _consume_shard_records(
    shard_id: str,
    stream_arn: str,
    shutdown_event: Event,
) -> None:
    """Retrieves the records from the shard and triggers processing"""
    shard_iterator = _get_shard_iterator(stream_arn, shard_id)
    batches: dict[Trigger, list[Record]] = defaultdict(list)

    for records in _get_shard_records(shard_id, shard_iterator):
        if not records:
            sleep(10)
            continue

        if shutdown_event.is_set():
            LOGGER.info("%s shutting down", shard_id)
            break

        for trigger in TRIGGERS:
            matching_records = tuple(
                record for record in records if trigger.records_filter(record)
            )

            if trigger.batch_size == 0:
                trigger.records_processor(matching_records)
                continue

            batches[trigger].extend(matching_records)
            if len(batches[trigger]) >= trigger.batch_size:
                batch = batches[trigger][: trigger.batch_size]
                trigger.records_processor(tuple(batch))
                batches[trigger] = batches[trigger][trigger.batch_size :]

        save_checkpoint(shard_id, records[-1].sequence_number)

    for trigger in TRIGGERS:
        if batch := batches[trigger]:
            trigger.records_processor(tuple(batch))
    LOGGER.info("%s shutdown gracefully", shard_id)


def consume() -> None:
    """Consumes the DynamoDB stream"""
    stream_arn = _get_stream_arn(TABLE_NAME)
    workers: list[Thread] = []
    shutdown_event = Event()

    for shards in _get_stream_shards(stream_arn):
        for shard in shards:
            shard_id: str = shard["ShardId"]
            is_closed = "EndingSequenceNumber" in shard["SequenceNumberRange"]

            if is_closed:
                remove_checkpoint(shard_id)
            else:
                worker = Thread(
                    args=(shard_id, stream_arn, shutdown_event),
                    daemon=True,
                    name=shard_id,
                    target=_consume_shard_records,
                )
                workers.append(worker)
                worker.start()

    def _shutdown(*_: Any) -> None:
        shutdown_event.set()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    LOGGER.info("Running with %s workers", len(workers))

    for worker in workers:
        worker.join()

    LOGGER.info("Stream consumption completed.")
