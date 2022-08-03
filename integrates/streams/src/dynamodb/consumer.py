import boto3
from dynamodb.replicator import (
    replicate,
)
from typing import (
    Any,
    Iterator,
    Optional,
)

CLIENT = boto3.client("dynamodbstreams")
MAX_ITEM_COUNT = 100
TABLE_NAME = "integrates_vms"


def _get_stream_arn(table_name: str) -> str:
    """Returns the ARN of the stream for the requested table"""
    response = CLIENT.list_streams(TableName=table_name)
    return response["Streams"][0]["StreamArn"]


def _describe_stream(
    exclusive_start_shard_id: Optional[str], stream_arn: str
) -> dict[str, Any]:
    """Returns information about a stream"""
    if exclusive_start_shard_id is None:
        args = {"StreamArn": stream_arn}
    else:
        args = {
            "ExclusiveStartShardId": exclusive_start_shard_id,
            "StreamArn": stream_arn,
        }

    return CLIENT.describe_stream(**args)


def _get_stream_shards(stream_arn: str) -> tuple[str, ...]:
    """Returns the shards for the requested stream"""
    open_shards = []
    current_shard_id = None

    while True:
        response = _describe_stream(current_shard_id, stream_arn)
        description = response["StreamDescription"]
        open_shards.extend(
            [
                shard
                for shard in description["Shards"]
                if "EndingSequenceNumber" not in shard["SequenceNumberRange"]
            ]
        )
        current_shard_id = description.get("LastEvaluatedShardId")

        if current_shard_id is None:
            break

    return tuple(open_shards)


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
    """
    Yields the records for the requested iterator

    This may keep going for up to 4 hours, so we need to limit the amount of
    records to process per execution.
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.LowLevel.Walkthrough.html
    """
    current_iterator = shard_iterator
    processed_records = 0

    while True:
        response = CLIENT.get_records(ShardIterator=shard_iterator)
        records = response["Records"]

        if records:
            processed_records += len(records)

            yield records

        current_iterator = response.get("NextShardIterator")

        if current_iterator is None or processed_records > MAX_ITEM_COUNT:
            break

    return tuple(records)


def consume() -> None:
    """Consumes the stream and triggers replication"""
    stream_arn = _get_stream_arn(TABLE_NAME)
    stream_shards = _get_stream_shards(stream_arn)

    for index, shard in enumerate(stream_shards):
        print(f"Working on shard {index + 1}/{len(stream_shards)}")
        shard_iterator = _get_shard_iterator(stream_arn, shard["ShardId"])

        for records in _get_shard_records(shard_iterator):
            replicate(records)
