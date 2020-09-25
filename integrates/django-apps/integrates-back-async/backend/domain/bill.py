# Standard library
from datetime import datetime
import io
import csv
from typing import (
    Dict,
    List,
)

# Local libraries
from backend.dal import (
    bill as bill_dal,
)

# Columns we want to show to the customers, with their correct names
# mapping to all possible names it may have in the data source
EXPECTED_COLUMNS: Dict[str, List[str]] = {
    'actor': ['actor'],
    'groups': ['groups'],
    'commit': ['commit', 'sha1'],
    'repository': ['repository'],
}


async def get_authors_data(
        *, date: datetime, group: str) -> List[Dict[str, str]]:
    buffer: io.BytesIO = await bill_dal.get_bill_buffer(
        date=date, group=group
    )
    buffer_str: io.StringIO = io.StringIO(buffer.read().decode())

    return [
        {
            column: next(value_generator, '-')
            for column, possible_names in EXPECTED_COLUMNS.items()
            for value_generator in [
                # This attempts to get the column value by trying the
                # possible names the column may have
                # this only yields truthy values (values with data)
                filter(None, (row.get(name) for name in possible_names)),
            ]
        }
        for row in csv.DictReader(buffer_str)
    ]
