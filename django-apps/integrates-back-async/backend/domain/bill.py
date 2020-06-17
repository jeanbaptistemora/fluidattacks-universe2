# Standard library
from datetime import datetime
import io
import csv
from typing import (
    Dict,
    List,
)

# Third party libraries
from asgiref.sync import sync_to_async

# Local libraries
from backend.dal import (
    bill as bill_dal,
)
from backend.utils import (
    apm,
)

# Constants
COLUMNS: Dict[str, str] = {
    # Map(original_bill -> parsed_bill)
    'actor': 'actor',
    'groups': 'groups',
    'organization': 'organization',
    'repository': 'repository',
    'sha1': 'commit',
}


@apm.trace()
@sync_to_async
def get_authors_data(*, date: datetime, group: str) -> List[Dict[str, str]]:
    buffer: io.BytesIO = bill_dal.get_bill_buffer(date=date, group=group)
    buffer_str: io.StringIO = io.StringIO(buffer.read().decode())

    return [
        {
            here_column: str(row.get(source_column, '-'))
            for source_column, here_column in COLUMNS.items()
        }
        for row in csv.DictReader(buffer_str)
    ]
