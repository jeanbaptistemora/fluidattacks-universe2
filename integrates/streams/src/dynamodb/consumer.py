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
    trigger_processors,
)
import logging
from threading import (
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
) -> Iterator[tuple[dict[str, Any], ...]]:
    """Yields the records for the requested iterator"""
    current_iterator = shard_iterator
    processed_records = 0

    while True:
        try:
            response = CLIENT.get_records(ShardIterator=current_iterator)
            records = tuple(response["Records"])

            if records:
                yield records

                processed_records += len(records)
                sequence_number = records[-1]["dynamodb"]["SequenceNumber"]

                save_checkpoint(shard_id, sequence_number)
                sleep(1)
            else:
                sleep(10)

            current_iterator = response.get("NextShardIterator")

            if current_iterator is None:
                LOGGER.warning("Shard closed, moving on")
                break
        except CLIENT.exceptions.ExpiredIteratorException:
            LOGGER.warning("Iterator expired, moving on")
            break

    LOGGER.info("%s processed %s records", shard_id, processed_records)


def _consume_shard_records(shard_id: str, stream_arn: str) -> None:
    """Retrieves the records from the shard and triggers processing"""
    shard_iterator = _get_shard_iterator(stream_arn, shard_id)

    for records in _get_shard_records(shard_id, shard_iterator):
        trigger_processors(records)


def consume() -> None:
    """Consumes the DynamoDB stream"""
    stream_arn = _get_stream_arn(TABLE_NAME)
    workers: list[Thread] = []

    for shards in _get_stream_shards(stream_arn):
        for shard in shards:
            shard_id = shard["ShardId"]
            is_closed = "EndingSequenceNumber" in shard["SequenceNumberRange"]

            if is_closed:
                remove_checkpoint(shard_id)
            else:
                worker = Thread(
                    args=(shard_id, stream_arn),
                    daemon=True,
                    target=_consume_shard_records,
                )
                workers.append(worker)
                worker.start()

    LOGGER.info("Running with %s workers", len(workers))

    for worker in workers:
        worker.join()

    LOGGER.info("Stream consumption completed.")
