# Standard libraries

# Third party libraries
from returns.io import IO

# Local libraries
from paginator import (
    PageId,
)
from tap_checkly.api.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


def list_alerts_channels(client: Client, page: PageId) -> IO[JSON]:
    return client.get(
        '/v1/alert-channels',
        params={'limit': page.per_page, 'page': page.page}
    )
