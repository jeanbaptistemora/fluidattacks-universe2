from target_redshift_2 import loader
from target_redshift_2.db_client.objects import SchemaID, TableID
from target_redshift_2.objects import RedshiftSchema
from target_redshift_2.singer import (
    SingerObject,
    SingerRecord,
    SingerSchema,
)


def test_process_lines_builder():
    # Arrange
    test_lines = [
        'json_test_schema',
        'json_test_record',
        'json_test_record_2'
    ]
    test_schema = SingerSchema(
        stream='stream_1',
        schema={"type": "object"},
        key_properties= frozenset(),
    )
    test_record = SingerRecord(stream='stream_1',record={"id": "123"})
    test_record_2 = SingerRecord(stream='stream_2',record={"id": "123"})

    def mock_deserialize(text: str) -> SingerObject:
        if text == 'json_test_schema':
            return test_schema
        if text == 'json_test_record':
            return test_record
        if text == 'json_test_record_2':
            return test_record_2
        raise Exception(f'Unexpected input: {text}')
    # Act
    process_lines = loader.process_lines_builder(mock_deserialize)
    result = process_lines(test_lines)
    # Assert=
    assert test_schema in result[0]
    assert test_record in result[1]
    assert test_record_2 in result[1]


def test_create_table_schema_map():
    # Arrange
    test_schemas = [
        SingerSchema(
            stream='the_table_0', schema={}, key_properties=frozenset()
        ),
        SingerSchema(
            stream='the_table_1', schema={}, key_properties=frozenset()
        ),
    ]

    def mock_to_rschema(s_schema: SingerSchema) -> RedshiftSchema:
        return RedshiftSchema(
            fields=frozenset(),
            schema_name='test_schema',
            table_name=s_schema.stream
        )
    # Act
    create_table_map = loader.create_table_schema_map_builder(mock_to_rschema)
    result = create_table_map(test_schemas)
    # Assert
    expected = [
        RedshiftSchema(
            fields=frozenset(),
            schema_name='test_schema',
            table_name='the_table_0'
        ),
        RedshiftSchema(
            fields=frozenset(),
            schema_name='test_schema',
            table_name='the_table_1'
        )
    ]
    for i in range(2):
        assert result[
            TableID(
                schema=SchemaID(None,schema_name=f'test_schema'),
                table_name=f'the_table_{i}'
            )
        ] == expected[i]
