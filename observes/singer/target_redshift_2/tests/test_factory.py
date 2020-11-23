# Standard libraries
from typing import FrozenSet
# Third party libraries
# Local libraries
from postgres_client.objects import DbTypes
from target_redshift_2.factory import (
    RedshiftRecordFactory,
    RedshiftSchemaFactory,
)
from target_redshift_2.objects import (
    RedshiftField,
    RedshiftRecord,
    RedshiftSchema,
)
from target_redshift_2.singer import (
    SingerRecord,
    SingerSchema,
)


def test_RedshiftSchemaFactory():
    factory: RedshiftSchemaFactory = RedshiftSchemaFactory()
    mock_s_schema = SingerSchema(
        'test_table',
        {
            'properties': {
                'field1': {"type": "number"}, 'field2': {"type": "string"}
            }
        },
        frozenset()
    )
    r_schema = factory.from_singer(
        mock_s_schema,
        'test_schema'
    )
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
    factory: RedshiftRecordFactory = RedshiftRecordFactory()
    mock_schema_fields: FrozenSet[RedshiftField] = frozenset({
        RedshiftField('field1', DbTypes.FLOAT),
        RedshiftField('field2', DbTypes.VARCHAR)
    })
    r_schema: RedshiftSchema = RedshiftSchema(
        mock_schema_fields,
        'test_schema',
        'test_table'
    )
    test_record = frozenset({'field1': 2.48, 'field2': 'text'}.items())
    r_record: RedshiftRecord = factory.from_singer(
        SingerRecord(
            'test_stream',
            test_record
        ),
        r_schema
    )
    expected_record = frozenset({'field1': "'2.48'", 'field2': "'text'"}.items())

    expected = RedshiftRecord(
        r_schema,
        expected_record
    )
    assert r_record == expected
