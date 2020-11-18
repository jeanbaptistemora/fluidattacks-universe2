from target_redshift_2 import loader
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
