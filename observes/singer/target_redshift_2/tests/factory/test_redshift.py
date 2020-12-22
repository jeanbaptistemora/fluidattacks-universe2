# Standard libraries
from typing import FrozenSet
# Third party libraries
# Local libraries
from postgres_client.table import DbTypes
from target_redshift_2.factory_pack import redshift
from target_redshift_2.factory_pack.redshift import RedshiftElementsFactory
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)


def test_rschema_creation():
    # Arrange
    factory: RedshiftElementsFactory = redshift.redshift_factory('test_schema')
    mock_s_schema = SingerSchema(
        'test_table',
        {
            'properties': {
                'field1': {"type": "number"}, 'field2': {"type": "string"}
            }
        },
        frozenset()
    )
    # Act
    r_schema = factory.to_rschema(mock_s_schema)
    # Assert
    expected = RedshiftSchema(
        frozenset({
            RedshiftField('field1', DbTypes.FLOAT),
            RedshiftField('field2', DbTypes.VARCHAR)
        }),
        'test_schema',
        'test_table'
    )
    assert r_schema == expected


def test_RedshiftRecordFactory():
    # Arrange
    factory: RedshiftElementsFactory = redshift.redshift_factory('test_schema')
    mock_schema_fields: FrozenSet[RedshiftField] = frozenset({
        RedshiftField('field1', DbTypes.FLOAT),
        RedshiftField('field2', DbTypes.VARCHAR)
    })
    mock_schema = RedshiftSchema(
        mock_schema_fields,
        'test_schema',
        'test_table'
    )
    test_record = frozenset({'field1': 2.48, 'field2': 'text'}.items())
    mock_record = SingerRecord('test_stream', test_record)
    # Act
    r_record: RedshiftRecord = factory.to_rrecord(mock_record, mock_schema)
    # Assert
    expected_record = frozenset(
        {'field1': "'2.48'", 'field2': "'text'"}.items()
    )
    expected = RedshiftRecord(mock_schema,expected_record)
    assert r_record == expected
