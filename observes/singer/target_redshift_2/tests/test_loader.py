from postgres_client.table import DbTypes, Table, TableID
from target_redshift_2 import loader
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)


class UnexpectedInput(Exception):
    pass


def test_create_table_schema_map_builder() -> None:
    # Arrange
    s_schema1 = SingerSchema(
        stream='the_table_1',
        schema={'field1': 'str'},
        key_properties=frozenset()
    )
    s_schema2 = SingerSchema(
        stream='the_table_1',
        schema={'field2': 'bool', 'field1': 'str'},
        key_properties=frozenset()
    )
    field1 = RedshiftField('field1', DbTypes.VARCHAR)
    field2 = RedshiftField('field2', DbTypes.BOOLEAN)
    test_table_id = TableID('test_schema', 'the_table_1')
    test_schemas = [s_schema1, s_schema2]

    def mock_to_rschema(s_schema: SingerSchema) -> RedshiftSchema:
        if s_schema == s_schema1:
            return RedshiftSchema(
                fields=frozenset({field1}),
                schema_name='test_schema',
                table_name=s_schema.stream
            )
        if s_schema == s_schema2:
            return RedshiftSchema(
                fields=frozenset({field2, field1}),
                schema_name='test_schema',
                table_name=s_schema.stream
            )
        raise UnexpectedInput()

    def mock_extract_table_id(r_schema: RedshiftSchema) -> TableID:
        # pylint: disable=unused-argument
        return test_table_id

    # Act
    create_table_map = loader.create_table_schema_map_builder(
        mock_to_rschema,
        mock_extract_table_id
    )
    result = create_table_map(test_schemas)
    # Assert
    expected = RedshiftSchema(
        fields=frozenset({field2, field1}),
        schema_name='test_schema',
        table_name='the_table_1'
    )
    assert result[test_table_id] == expected


def test_create_redshift_records_builder() -> None:
    # Arrange
    s_record1 = SingerRecord('table_1', {})
    s_record2 = SingerRecord('table_2', {})
    r_schema1 = RedshiftSchema(
        frozenset({RedshiftField('field1', DbTypes.BOOLEAN)}),
        'test_schema', 'test_table'
    )
    r_schema2 = RedshiftSchema(
        frozenset({RedshiftField('field2', DbTypes.FLOAT)}),
        'test_schema', 'test_table_2'
    )
    table_id1 = TableID('test_schema', 'table1')
    table_id2 = TableID('test_schema_2', 'table2')
    r_record1 = RedshiftRecord(r_schema1, frozenset())
    r_record2 = RedshiftRecord(r_schema2, frozenset())
    test_records = [s_record1, s_record2]
    test_map = {table_id1: r_schema1, table_id2: r_schema2}

    def mock_to_rrecord(
        s_record: SingerRecord, r_schema: RedshiftSchema
    ) -> RedshiftRecord:
        if s_record == s_record1 and r_schema == r_schema1:
            return r_record1
        if s_record == s_record2 and r_schema == r_schema2:
            return r_record2
        raise UnexpectedInput()

    def mock_to_extract_table_id(s_record: SingerRecord) -> TableID:
        if s_record == s_record1:
            return table_id1
        if s_record == s_record2:
            return table_id2
        raise UnexpectedInput()

    # Act
    create_rrecords = loader.create_redshift_records_builder(
        mock_to_rrecord, mock_to_extract_table_id
    )
    result = create_rrecords(test_records, test_map)
    # Assert
    assert r_record1 in result
    assert r_record2 in result


def test_create_table_mapper_builder() -> None:
    # Arrange
    test_table_id = TableID('test_schema', 'test_table')
    test_table = Table(
        id=test_table_id,
        primary_keys=frozenset(),
        columns=frozenset({}),
        table_path=lambda x: x,
        add_columns=lambda x: x,
    )

    def mock_retrieve_table(table_id: TableID) -> Table:
        if table_id == test_table_id:
            return test_table
        raise UnexpectedInput()

    # Act
    create_table_map = loader.create_table_mapper_builder(
        mock_retrieve_table
    )
    result = create_table_map([test_table_id])
    # Assert
    assert result[test_table_id] == test_table
