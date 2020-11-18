from target_redshift_2 import loader
from target_redshift_2.db_client.objects import (
    DbTypes,
    SchemaID,
    TableID,
)
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)
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


def test_create_table_schema_map_builder():
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


def test_create_redshift_records_builder():
    s_record1 = SingerRecord('table_1', {})
    s_record2 = SingerRecord('table_2', {})
    r_schema1 = RedshiftSchema(
        frozenset({RedshiftField('field1',DbTypes.BOOLEAN)}),
        'test_schema', 'test_table'
    )
    r_schema2 = RedshiftSchema(
        frozenset({RedshiftField('field2',DbTypes.FLOAT)}),
        'test_schema', 'test_table_2'
    )
    table_id1 = TableID(SchemaID(None, 'test_schema'), 'table1')
    table_id2 = TableID(SchemaID(None, 'test_schema_2'), 'table2')
    r_record1 = RedshiftRecord(r_schema1,frozenset())
    r_record2 = RedshiftRecord(r_schema2,frozenset())
    test_records = [s_record1, s_record2]
    test_map = {table_id1: r_schema1, table_id2: r_schema2}

    def mock_to_rrecord(
        s_record: SingerRecord, r_schema: RedshiftSchema
    ) -> RedshiftRecord:
        if s_record == s_record1 and r_schema == r_schema1:
            return r_record1
        if s_record == s_record2 and r_schema == r_schema2:
            return r_record2
        raise Exception(f'Unexpected input')

    def mock_to_extract_table_id(s_record: SingerRecord) -> TableID:
        if s_record == s_record1:
            return table_id1
        if s_record == s_record2:
            return table_id2
        raise Exception(f'Unexpected input')

    # Act
    create_rrecords = loader.create_redshift_records_builder(
        mock_to_rrecord, mock_to_extract_table_id
    )
    result = create_rrecords(test_records, test_map)
    # Assert
    assert r_record1 in result
    assert r_record2 in result
