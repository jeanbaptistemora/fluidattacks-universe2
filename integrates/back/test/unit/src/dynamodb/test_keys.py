from dynamodb import (
    keys,
)
from dynamodb.types import (
    Facet,
    PrimaryKey,
)
import pytest


def test_build_key_only_pk() -> None:
    key = keys.build_key(
        facet=Facet(attrs=tuple(), pk_alias="ENTITY1#name", sk_alias=""),
        values={"name": "unittesting"},
    )
    assert key == PrimaryKey(partition_key="ENTITY1#unittesting", sort_key="")


def test_build_key_partial() -> None:
    key = keys.build_key(
        facet=Facet(
            attrs=tuple(), pk_alias="ENTITY1#name", sk_alias="ENTITY2#id"
        ),
        values={"name": "unittesting"},
    )
    assert key == PrimaryKey(
        partition_key="ENTITY1#unittesting", sort_key="ENTITY2"
    )


def test_build_key_pk_and_sk() -> None:
    key = keys.build_key(
        facet=Facet(
            attrs=tuple(), pk_alias="ENTITY1#name", sk_alias="ENTITY2#id"
        ),
        values={"id": "123", "name": "unittesting"},
    )
    assert key == PrimaryKey(
        partition_key="ENTITY1#unittesting", sort_key="ENTITY2#123"
    )


def test_build_key_composite_sk() -> None:
    key = keys.build_key(
        facet=Facet(
            attrs=tuple(),
            pk_alias="ENTITY1#name",
            sk_alias="ENTITY2#id#HIST#date",
        ),
        values={
            "date": "2020-11-19T13:39:56+00:00",
            "id": "123",
            "name": "unittesting",
        },
    )
    assert key == PrimaryKey(
        partition_key="ENTITY1#unittesting",
        sort_key="ENTITY2#123#HIST#2020-11-19T13:39:56+00:00",
    )


def test_build_key_reserved_words() -> None:
    with pytest.raises(ValueError):
        keys.build_key(
            facet=Facet(attrs=tuple(), pk_alias="ENTITY1#name", sk_alias=""),
            values={"name#something#else": "unittesting"},
        )
