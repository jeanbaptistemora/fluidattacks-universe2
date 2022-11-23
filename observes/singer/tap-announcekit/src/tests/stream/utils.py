from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)


def test_schema(s_schema: SingerSchema) -> None:
    assert all(
        k in s_schema.schema.raw_schema["properties"].keys()
        for k in s_schema.key_properties
    )


def test_schema_record(s_schema: SingerSchema, s_record: SingerRecord) -> None:
    jschema = s_schema.schema
    jrecord = s_record.record
    assert frozenset(jschema.raw_schema["properties"].keys()) == frozenset(
        jrecord.keys()
    )
    assert len(jschema.raw_schema["properties"]) == len(jrecord.keys())
