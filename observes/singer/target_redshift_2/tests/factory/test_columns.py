# Standard libraries
# Third party libraries
# Local libraries
from postgres_client.table import (
    DbTypes,
    IsolatedColumn,
)
from target_redshift_2.factory_pack import columns
from target_redshift_2.objects import RedshiftField


def test_from_rfield():
    # Arrange
    field1 = RedshiftField('field1', DbTypes.BOOLEAN)
    # Act
    result = columns.from_rfield(field1)
    # Assert
    expected = IsolatedColumn(
        name=field1.name, field_type=DbTypes.BOOLEAN.value, default_val=None
    )
    assert result == expected
