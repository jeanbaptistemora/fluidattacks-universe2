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


def _mask_env_vars(result: Iterator[JSON]) -> None:
    for item in result:
        env_vars = item['environmentVariables']
        vars_list = env_vars if env_vars else []
        for env_var in vars_list:
            env_var['value'] = '__masked__'


def list_checks(client: Client, page: PageId) -> IO[Iterator[JSON]]:
    result = client.get(
        '/v1/checks',
        params={'limit': page.per_page, 'page': page.page}
    )
    _mask_env_vars(result)
    LOG.debug('checks response: %s', result)
    return IO(result)


def list_check_groups(client: Client, page: PageId) -> IO[Iterator[JSON]]:
    result = client.get(
        '/v1/check-groups',
        params={'limit': page.per_page, 'page': page.page}
    )
    _mask_env_vars(result)
    LOG.debug('check-groups response: %s', result)
    return IO(result)


def list_check_status(client: Client) -> IO[Iterator[JSON]]:
    result = client.get('/v1/check-statuses')
    LOG.debug('check-status response: %s', result)
    return IO(result)
