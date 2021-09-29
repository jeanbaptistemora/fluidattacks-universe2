from dynamodb import (
    table,
)
from dynamodb.types import (
    Facet,
    Index,
    PrimaryKey,
    Table,
)


def test_load_tables() -> None:
    result = table.load_tables(
        {
            "DataModel": [
                {
                    "GlobalSecondaryIndexes": [
                        {
                            "IndexName": "test_index",
                            "KeyAttributes": {
                                "PartitionKey": {
                                    "AttributeName": "sk",
                                    "AttributeType": "S",
                                },
                                "SortKey": {
                                    "AttributeName": "pk",
                                    "AttributeType": "S",
                                },
                            },
                        }
                    ],
                    "KeyAttributes": {
                        "PartitionKey": {
                            "AttributeName": "pk",
                            "AttributeType": "S",
                        },
                        "SortKey": {
                            "AttributeName": "sk",
                            "AttributeType": "S",
                        },
                    },
                    "TableFacets": [
                        {
                            "FacetName": "test_facet",
                            "KeyAttributeAlias": {
                                "PartitionKeyAlias": "ENTITY1#name",
                                "SortKeyAlias": "ENTITY2#id",
                            },
                            "NonKeyAttributes": ["attr1", "attr2", "attr3"],
                        },
                    ],
                    "TableName": "test_table",
                }
            ]
        }
    )
    assert result[0] == Table(
        facets={
            "test_facet": Facet(
                attrs=("attr1", "attr2", "attr3"),
                pk_alias="ENTITY1#name",
                sk_alias="ENTITY2#id",
            )
        },
        indexes={
            "test_index": Index(
                name="test_index",
                primary_key=PrimaryKey(partition_key="sk", sort_key="pk"),
            )
        },
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
    )
