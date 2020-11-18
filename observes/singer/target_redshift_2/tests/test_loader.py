from typing import FrozenSet, List
from target_redshift_2 import loader
from target_redshift_2.db_client.objects import (
    CursorExeAction, DbTypes, IsolatedColumn,
    SchemaID,
    Table,
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
    s_schema1 = SingerSchema(
        stream='the_table_1', schema={'field1': 'str'}, key_properties=frozenset()
    )
    s_schema2 = SingerSchema(
        stream='the_table_1',
        schema={'field2': 'bool', 'field1': 'str'},
        key_properties=frozenset()
    )
    field1 = RedshiftField('field1', DbTypes.VARCHAR)
    field2 = RedshiftField('field2', DbTypes.BOOLEAN)
    test_table_id = TableID(SchemaID(None, 'test_schema'), 'the_table_1')
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
        raise Exception(f'Unexpected input')

    def mock_extract_table_id(r_schema: RedshiftSchema) -> TableID:
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


def test_create_redshift_records_builder():
    # Arrange
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


def test_create_table_mapper_builder():
    # Arrange
    test_table_id = TableID(SchemaID(None, 'test_schema'), 'test_table')
    test_table = Table(
        id=test_table_id,
        primary_keys=frozenset(),
        columns=frozenset({}),
        prototype=None
    )

    def mock_retrieve_table(table_id: TableID) -> Table:
        if table_id == test_table_id:
            return test_table
        raise Exception(f'Unexpected input')

    # Act
    create_table_map = loader.create_table_mapper_builder(
        mock_retrieve_table
    )
    result = create_table_map([test_table_id])
    # Assert
    assert result[test_table_id] == test_table


def test_update_schema_builder():
    # Arrange
    test_table_id = TableID(SchemaID(None, 'test_schema'), 'test_table')
    test_table = Table(
        id=test_table_id,
        primary_keys=frozenset(),
        columns=frozenset({}),
        prototype=None
    )
    test_schema = RedshiftSchema(frozenset(), 'the_schema', 'the_table')
    test_columns = frozenset({IsolatedColumn('field1','bool')})
    test_table_map = {test_table_id: test_table}
    test_table_schema_map = {test_table_id: test_schema}
    action_executed = {'executed': False}

    def mock_to_columns(rschema: RedshiftSchema) -> FrozenSet[IsolatedColumn]:
        if rschema == test_schema:
            return test_columns
        raise Exception(f'Unexpected input')

    def mock_action():
        action_executed['executed'] = True

    def mock_add_columns(
        table: Table, columns: FrozenSet[IsolatedColumn]
    ) -> List[CursorExeAction]:
        if table == test_table and columns == test_columns:
            return [
                CursorExeAction(
                    cursor=None, act=mock_action, statement='the_statement'
                )
            ]
        raise Exception(f'Unexpected input')

    # Act
    update_schema = loader.update_schema_builder(
        mock_to_columns,
        mock_add_columns
    )
    update_schema(test_table_map, test_table_schema_map)
    # Assert
    assert action_executed['executed'] == True
