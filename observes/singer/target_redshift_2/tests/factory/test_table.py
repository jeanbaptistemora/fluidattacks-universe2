from postgres_client.table import (
    DbTypes,
    IsolatedColumn,
    TableDraft,
    TableID,
)
from target_redshift_2.factory_pack import table
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftSchema,
)
from singer_io.singer import SingerRecord


def test_tabledraft_factory() -> None:
    # Arrange
    test_schema = 'the_schema'
    factory = table.tabledraft_factory(test_schema)
    field1 = RedshiftField('field1', DbTypes.BOOLEAN)
    field2 = RedshiftField('field2', DbTypes.NUMERIC)
    column1 = IsolatedColumn(
        name='field1', field_type=DbTypes.BOOLEAN.value, default_val=None
    )
    column2 = IsolatedColumn(
        name='field2', field_type=DbTypes.NUMERIC.value, default_val=None
    )
    test_rschema = RedshiftSchema(
        fields=frozenset({field1, field2}),
        schema_name=test_schema,
        table_name='super_table'
    )
    test_table_id = TableID(
        test_schema, table_name='super_table'
    )
    # Act
    result = factory.rschema_to_tdraft(test_rschema)
    # Assert
    expected = TableDraft(
        id=test_table_id,
        primary_keys=frozenset(),
        columns=frozenset({column1, column2})
    )
    assert result == expected


def test_tid_factory_rschema_to_tid() -> None:
    # Arrange
    test_schema = 'the_schema'
    factory = table.tableid_factory(test_schema)
    test_rschema = RedshiftSchema(
        fields=frozenset(),
        schema_name='the_schema',
        table_name='super_table'
    )
    # Act
    result = factory.rschema_to_tid(test_rschema)
    # Assert
    expected = TableID(
        schema=test_schema,
        table_name='super_table'
    )
    assert result == expected


def test_tid_factory_srecord_to_tid() -> None:
    # Arrange
    test_schema = 'the_schema'
    factory = table.tableid_factory(test_schema)
    test_srecord = SingerRecord(stream='table1', record={})
    # Act
    result = factory.srecord_to_tid(test_srecord)
    # Assert
    expected = TableID(
        schema=test_schema,
        table_name='table1'
    )
    assert result == expected
