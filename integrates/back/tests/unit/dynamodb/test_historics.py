from dynamodb import (
    historics,
)
from dynamodb.types import (
    Facet,
    PrimaryKey,
)


def test_get_metadata() -> None:
    metadata = historics.get_metadata(
        item_id="ENTITY1#unittesting",
        key_structure=PrimaryKey(partition_key="sk", sort_key="pk"),
        raw_items=(
            {"pk": "ENTITY1#unittesting", "sk": "ENTITY2#123"},
            {"pk": "ENTITY1#unittesting#STATE", "sk": "ENTITY2#123"},
        ),
    )
    assert metadata == {"pk": "ENTITY1#unittesting", "sk": "ENTITY2#123"}


def test_get_latest() -> None:
    latest_state = historics.get_latest(
        item_id="ENTITY1#unittesting",
        key_structure=PrimaryKey(partition_key="sk", sort_key="pk"),
        historic_suffix="STATE",
        raw_items=(
            {"pk": "ENTITY1#unittesting", "sk": "ENTITY2#123"},
            {"pk": "ENTITY1#unittesting#STATE", "sk": "ENTITY2#123"},
            {"pk": "ENTITY1#unittesting#STATE2", "sk": "ENTITY2#123"},
        ),
    )
    assert latest_state == {
        "pk": "ENTITY1#unittesting#STATE",
        "sk": "ENTITY2#123",
    }


def test_build_historic() -> None:
    items = historics.build_historic(
        attributes={"attr1": "val1"},
        historic_facet=Facet(
            attrs=tuple(), pk_alias="ENTITY2#id", sk_alias="STATE#date"
        ),
        key_structure=PrimaryKey(partition_key="pk", sort_key="sk"),
        key_values={
            "date": "2020-11-19T13:39:56+00:00",
            "id": "123",
            "name": "unittesting",
        },
        latest_facet=Facet(
            attrs=tuple(), pk_alias="ENTITY2#id#STATE", sk_alias="ENTITY1#name"
        ),
    )
    assert items == (
        {
            "pk": "ENTITY2#123#STATE",
            "sk": "ENTITY1#unittesting",
            "attr1": "val1",
        },
        {
            "pk": "ENTITY2#123",
            "sk": "STATE#2020-11-19T13:39:56+00:00",
            "attr1": "val1",
        },
    )
