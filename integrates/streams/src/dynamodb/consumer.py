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

ENDPOINT = (
    f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"
    if FI_ENVIRONMENT == "dev"
    else None
)
CLIENT = SESSION.client(endpoint_url=ENDPOINT, service_name="dynamodbstreams")
TABLE_NAME = "integrates_vms"
RESOURCE = SESSION.resource(endpoint_url=ENDPOINT, service_name="dynamodb")
TABLE_RESOURCE = RESOURCE.Table(TABLE_NAME)


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


def _get_shard_checkpoint(shard_id: str) -> Optional[str]:
    """Returns the last known iterator for the requested shard"""
    response = TABLE_RESOURCE.get_item(
        Key={"pk": f"SHARD#{shard_id}", "sk": f"SHARD#{shard_id}"}
    )
    item = response.get("Item")

    if item:
        return item["last_iterator"]

    return None


def _get_shard_iterator(stream_arn: str, shard_id: str) -> str:
    """Returns the iterator id for the requested shard"""
    shard_checkpoint = _get_shard_checkpoint(shard_id)

    if shard_checkpoint:
        return shard_checkpoint

    response = CLIENT.get_shard_iterator(
        ShardId=shard_id,
        ShardIteratorType="LATEST",
        StreamArn=stream_arn,
    )

    return response["ShardIterator"]


def _save_shard_checkpoint(shard_id: str, last_iterator: str) -> None:
    TABLE_RESOURCE.put_item(
        Item={
            "pk": f"SHARD#{shard_id}",
            "sk": f"SHARD#{shard_id}",
            "last_iterator": last_iterator,
        }
    )


def _get_shard_records(
    shard_id: str,
    shard_iterator: str,
) -> Iterator[tuple[dict[str, Any], ...]]:
    """Yields the records for the requested iterator"""
    current_iterator = shard_iterator
    processed_batches = 0
    processed_records = 0

    while True:
        try:
            response = CLIENT.get_records(ShardIterator=current_iterator)
            records = tuple(response["Records"])
            processed_batches += 1
            processed_records += len(records)

            if processed_batches % 10 == 0:
                _save_shard_checkpoint(shard_id, current_iterator)

            if records:
                yield records
                sleep(1)
            else:
                sleep(10)

            current_iterator = response.get("NextShardIterator")

            if current_iterator is None:
                print("Shard closed, moving on")
                break
        except CLIENT.exceptions.ExpiredIteratorException:
            print("Iterator expired, moving on")
            break

    print("Processed", processed_records, "records")


def _consume_shard_records(shard: dict[str, Any], stream_arn: str) -> None:
    """Retrieves the records from the shard and triggers processing"""
    shard_id = shard["ShardId"]
    shard_iterator = _get_shard_iterator(stream_arn, shard_id)

    for records in _get_shard_records(shard_id, shard_iterator):
        process(records)


def _remove_shard_checkpoint(shard: dict[str, Any]) -> None:
    """Removes a checkpoint in the database"""
    shard_id = shard["ShardId"]

    TABLE_RESOURCE.delete_item(
        Key={"pk": f"SHARD#{shard_id}", "sk": f"SHARD#{shard_id}"}
    )


def consume() -> None:
    """Consumes the DynamoDB stream"""
    stream_arn = _get_stream_arn(TABLE_NAME)
    workers: list[Thread] = []

    for shards in _get_stream_shards(stream_arn):
        for shard in shards:
            is_closed = "EndingSequenceNumber" in shard["SequenceNumberRange"]

            if is_closed:
                _remove_shard_checkpoint(shard)
            else:
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
