from postgres_client.table import (
    IsolatedColumn,
)
from target_redshift_2.objects import (
    RedshiftField,
)


def from_rfield(r_field: RedshiftField) -> IsolatedColumn:
    """Transform `RedshiftField` into a `IsolatedColumn`"""
    return IsolatedColumn(
        name=r_field.name, field_type=r_field.dbtype.value, default_val=None
    )
