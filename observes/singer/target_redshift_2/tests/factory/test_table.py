from target_redshift_2.db_client.objects import DbTypes, IsolatedColumn, SchemaID, TableDraft, TableID
from target_redshift_2.factory_pack import table
from target_redshift_2.objects import RedshiftField, RedshiftSchema


def test_from_rschema_builder():
    # Arrange
    field1 = RedshiftField('field1', DbTypes.BOOLEAN)
    field2 = RedshiftField('field2', DbTypes.NUMERIC)
    column1 = IsolatedColumn(
        name='field1', field_type='bool', default_val='False'
    )
    column2 = IsolatedColumn(
        name='field2', field_type='numeric', default_val='0'
    )

    def mock_from_rfield(rfield: RedshiftField) -> IsolatedColumn:
        if rfield == field1:
            return column1
        if rfield == field2:
            return column2
        raise Exception('Unexpected input')

    from_rschema = table.from_rschema_builder(mock_from_rfield)
    test_rschema = RedshiftSchema(
        fields=frozenset({field1, field2}),
        schema_name='the_schema',
        table_name='super_table'
    )
    # Act
    result = from_rschema(test_rschema)
    # Assert
    expected_id = TableID(
        SchemaID(None, 'the_schema'), table_name='super_table'
    )
    expected = TableDraft(
        id=expected_id,
        primary_keys=frozenset(),
        columns=frozenset({column1, column2})
    )
    assert result == expected
