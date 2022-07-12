from fa_purity.pure_iter.factory import (
    pure_map,
)
from redshift_client.column import (
    Column,
)
from redshift_client.data_type.core import (
    PrecisionType,
    PrecisionTypes,
)
from redshift_client.sql_client import (
    RowData,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.table.core import (
    Table,
)


def _truncate_str(column: Column, item: PrimitiveVal) -> PrimitiveVal:
    if isinstance(column.data_type.value, PrecisionType):
        if column.data_type.value.data_type in (
            PrecisionTypes.CHAR,
            PrecisionTypes.VARCHAR,
        ):
            if isinstance(item, str):
                return item[0 : column.data_type.value.precision]
            raise Exception("`CHAR` or `VARCHAR` item must be an str instance")
    return item


def truncate_row(table: Table, row: RowData) -> RowData:
    columns = pure_map(
        lambda c: (c[0], table.columns[c[1]]), tuple(enumerate(table.order))
    )
    trucated = columns.map(lambda c: _truncate_str(c[1], row.data[c[0]]))
    return RowData(tuple(trucated))
