from postgres_client.connection import ConnectionID
from postgres_client.table import DbTypes, IsolatedColumn, TableDraft, TableID
from target_redshift_2.factory_pack import table
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftSchema,
)
from target_redshift_2.singer import SingerRecord


def test_draft_from_rschema_builder():
    # Arrange
    field1 = RedshiftField('field1', DbTypes.BOOLEAN)
    field2 = RedshiftField('field2', DbTypes.NUMERIC)
    column1 = IsolatedColumn(
        name='field1', field_type='bool', default_val='False'
    )
    column2 = IsolatedColumn(
        name='field2', field_type='numeric', default_val='0'
    )
    test_rschema = RedshiftSchema(
        fields=frozenset({field1, field2}),
        schema_name='the_schema',
        table_name='super_table'
    )
    test_table_id = TableID(
        'the_schema', table_name='super_table'
    )

    def mock_column_from_rfield(rfield: RedshiftField) -> IsolatedColumn:
        if rfield == field1:
            return column1
        if rfield == field2:
            return column2
        raise Exception('Unexpected input')

    def mock_tid_from_rschema(rfield: RedshiftSchema) -> TableID:
        if rfield == test_rschema:
            return test_table_id
        raise Exception('Unexpected input')

    # Act
    from_rschema = table.draft_from_rschema_builder(
        mock_column_from_rfield, mock_tid_from_rschema
    )
    result = from_rschema(test_rschema)
    # Assert
    expected = TableDraft(
        id=test_table_id,
        primary_keys=frozenset(),
        columns=frozenset({column1, column2})
    )
    assert result == expected


def test_tid_from_rschema():
    # Arrange
    test_rschema = RedshiftSchema(
        fields=frozenset(),
        schema_name='the_schema',
        table_name='super_table'
    )
    # Act
    from_rschema = table.tid_from_rschema
    result = from_rschema(test_rschema)
    # Assert
    expected = TableID(
        schema='the_schema',
        table_name='super_table'
    )
    assert result == expected


def test_tid_from_srecord_builder():
    # Arrange
    test_connection = ConnectionID(
        'the_db', 'super_user', '1234', 'the_host', '9000'
    )
    test_schema = 'the_schema'
    test_srecord = SingerRecord(stream='table1', record={})
    # Act
    from_srecord = table.tid_from_srecord_builder(test_schema)
    result = from_srecord(test_srecord)
    # Assert
    expected = TableID(
        schema=test_schema,
        table_name='table1'
    )
    assert result == expected
