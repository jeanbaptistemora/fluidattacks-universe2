from dynamodb.types import (
    Facet,
    Index,
    PrimaryKey,
    Table,
)
from typing import (
    Any,
)


def _load_facets(facets: tuple[dict[str, Any], ...]) -> dict[str, Facet]:
    return {
        facet["FacetName"]: Facet(
            attrs=tuple(facet.get("NonKeyAttributes", [])),
            pk_alias=facet["KeyAttributeAlias"]["PartitionKeyAlias"],
            sk_alias=facet["KeyAttributeAlias"]["SortKeyAlias"],
        )
        for facet in facets
    }


def _get_key(key_attrs: dict[str, Any]) -> PrimaryKey:
    return PrimaryKey(
        partition_key=key_attrs["PartitionKey"]["AttributeName"],
        sort_key=key_attrs["SortKey"]["AttributeName"],
    )


def _load_indexes(indexes: tuple[dict[str, Any], ...]) -> dict[str, Index]:
    return {
        index["IndexName"]: Index(
            name=index["IndexName"],
            primary_key=_get_key(index["KeyAttributes"]),
        )
        for index in indexes
    }


def load_tables(model: dict[str, Any]) -> tuple[Table, ...]:
    tables: tuple[dict[str, Any], ...] = model["DataModel"]

    return tuple(
        Table(
            name=table["TableName"],
            primary_key=_get_key(table["KeyAttributes"]),
            facets=_load_facets(tuple(table["TableFacets"])),
            indexes=_load_indexes(tuple(table["GlobalSecondaryIndexes"])),
        )
        for table in tables
    )
