from dynamodb.context import (
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)
from dynamodb.processor import (
    process,
)
from dynamodb.utils import (
    SESSION,
)
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

CLIENT = SESSION.client(
    endpoint_url=(
        f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"
        if FI_ENVIRONMENT == "dev"
        else None
    ),
    service_name="dynamodbstreams",
)
TABLE_NAME = "integrates_vms"


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
    """Yields the open shards for the requested stream"""
    current_shard_id = None

    while True:
        response = _describe_stream(current_shard_id, stream_arn)
        description = response["StreamDescription"]
        open_shards = tuple(
            shard
            for shard in description["Shards"]
            if "EndingSequenceNumber" not in shard["SequenceNumberRange"]
        )

        yield open_shards

        current_shard_id = description.get("LastEvaluatedShardId")

        if current_shard_id is None:
            break


def _get_shard_iterator(stream_arn: str, shard_id: str) -> str:
    """Returns the id of the iterator for the requested shard"""
    response = CLIENT.get_shard_iterator(
        ShardId=shard_id,
        ShardIteratorType="LATEST",
        StreamArn=stream_arn,
    )

    return response["ShardIterator"]


def _get_shard_records(
    shard_iterator: str,
) -> Iterator[tuple[dict[str, Any], ...]]:
    """Yields the records for the requested iterator"""
    current_iterator = shard_iterator
    processed_records = 0

    while True:
        try:
            response = CLIENT.get_records(ShardIterator=shard_iterator)
        except CLIENT.exceptions.ExpiredIteratorException:
            print("Iterator expired, moving on")
            break

        records = tuple(response["Records"])

        if records:
            processed_records += len(records)

            yield records
        else:
            sleep(10)

        current_iterator = response.get("NextShardIterator")

        if current_iterator is None:
            break

    print("Processed", processed_records, "records")


def _consume_shard_records(shard: dict[str, Any], stream_arn: str) -> None:
    """Retrieves the records from the shard and triggers replication"""
    shard_iterator = _get_shard_iterator(stream_arn, shard["ShardId"])

    for records in _get_shard_records(shard_iterator):
        process(records)


def consume() -> None:
    """Consumes the DynamoDB stream"""
    stream_arn = _get_stream_arn(TABLE_NAME)
    workers: list[Thread] = []

    for shards in _get_stream_shards(stream_arn):
        for shard in shards:
            worker = Thread(
                args=(shard, stream_arn),
                daemon=True,
                target=_consume_shard_records,
            )
            workers.append(worker)
            worker.start()

    print("Running with", len(workers), "workers")

    for worker in workers:
        worker.join()

    print("Stream consumption completed.")
