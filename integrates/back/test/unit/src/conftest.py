import asyncio
import logging
import pytest
from settings import (
    LOGGING,
)
from typing import (
    Any,
    AsyncGenerator,
)

logging.config.dictConfig(LOGGING)


@pytest.fixture(autouse=True)
def disable_logging() -> None:
    """Disable logging in all tests."""
    logging.disable(logging.INFO)


@pytest.yield_fixture(scope="session")
def event_loop() -> AsyncGenerator[Any, None]:  # type: ignore
    loop = asyncio.get_event_loop_policy().new_event_loop()
    # Exception: WF(AsyncGenerator is subtype of iterator)
    yield loop  # NOSONAR
    loop.close()


@pytest.fixture(scope="session")
def dynamodb_tables_args() -> dict:
    tables = dict(
        integrates_vms=dict(
            key_schema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            attribute_definitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "pk_2", "AttributeType": "S"},
                {"AttributeName": "pk_3", "AttributeType": "S"},
                {"AttributeName": "pk_4", "AttributeType": "S"},
                {"AttributeName": "pk_5", "AttributeType": "S"},
                {"AttributeName": "pk_6", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
                {"AttributeName": "sk_2", "AttributeType": "S"},
                {"AttributeName": "sk_3", "AttributeType": "S"},
                {"AttributeName": "sk_4", "AttributeType": "S"},
                {"AttributeName": "sk_5", "AttributeType": "S"},
                {"AttributeName": "sk_6", "AttributeType": "S"},
            ],
            global_secondary_indexes=[
                {
                    "IndexName": "inverted_index",
                    "KeySchema": [
                        {"AttributeName": "sk", "KeyType": "HASH"},
                        {"AttributeName": "pk", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "gsi_2",
                    "KeySchema": [
                        {"AttributeName": "pk_2", "KeyType": "HASH"},
                        {"AttributeName": "sk_2", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "gsi_3",
                    "KeySchema": [
                        {"AttributeName": "pk_3", "KeyType": "HASH"},
                        {"AttributeName": "sk_3", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "gsi_4",
                    "KeySchema": [
                        {"AttributeName": "pk_4", "KeyType": "HASH"},
                        {"AttributeName": "sk_4", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "gsi_5",
                    "KeySchema": [
                        {"AttributeName": "pk_5", "KeyType": "HASH"},
                        {"AttributeName": "sk_5", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
                {
                    "IndexName": "gsi_6",
                    "KeySchema": [
                        {"AttributeName": "pk_6", "KeyType": "HASH"},
                        {"AttributeName": "sk_6", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
            ],
            provisioned_throughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        )
    )
    return tables
