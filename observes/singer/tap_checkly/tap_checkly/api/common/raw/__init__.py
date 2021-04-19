# Standard libraries
import logging

# Third party libraries
from typing import (
    Iterator,
)
from returns.io import (
    IO,
)

# Local libraries
from paginator import (
    PageId,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.common import (
    JSON,
)


LOG = logging.getLogger(__name__)


def list_alerts_channels(client: Client, page: PageId) -> IO[Iterator[JSON]]:
    result = client.get(
        '/v1/alert-channels',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('alert-channels response: %s', result)
    return IO(result)
