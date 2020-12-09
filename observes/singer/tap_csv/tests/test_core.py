from typing import Dict
from tap_csv import core
from tap_csv.core import ColumnType


def test_translate_types() -> None:
    # Arrange
    test_types: Dict[str, ColumnType] = {
        'field1': ColumnType.STRING,
        'field2': ColumnType.NUMBER,
        'field3': ColumnType.DATE_TIME,
    }
    # Act
    result = core.translate_types(test_types)
    # Assert
    expected = {
        'field1': {"type": "string"},
        'field2': {"type": ["number", "null"]},
        'field3': {"type": ["string", "null"]}
    }
    assert result == expected
