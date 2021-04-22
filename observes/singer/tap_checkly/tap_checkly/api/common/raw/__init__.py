# Standard libraries
import logging

# Third party libraries
from typing import (
    List,
)
from requests.exceptions import (
    HTTPError,
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


def _mask_env_vars(result: List[JSON]) -> None:
    for item in result:
        env_vars = item['environmentVariables']
        vars_list = env_vars if env_vars else []
        for env_var in vars_list:
            env_var['value'] = '__masked__'


def get_report(
    client: Client,
    check_id: str,
) -> IO[JSON]:
    result = client.get(f'/v1/reporting/{check_id}')
    LOG.debug('reports response: %s', result)
    return IO(result)


def list_alerts_channels(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/alert-channels',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('alert-channels response: %s', result)
    return IO(result)


def list_checks(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/checks',
        params={'limit': page.per_page, 'page': page.page}
    )
    _mask_env_vars(result)
    LOG.debug('checks response: %s', result)
    return IO(result)


def list_check_groups(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/check-groups',
        params={'limit': page.per_page, 'page': page.page}
    )
    _mask_env_vars(result)
    LOG.debug('check-groups response: %s', result)
    return IO(result)


def list_check_results(
    client: Client,
    check_id: str,
    page: PageId
) -> IO[List[JSON]]:
    result = client.get(
        f'/v1/check-results-rolled-up/{check_id}',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('check-results-rolled-up response: %s', result)
    LOG.info('Getting check-results %s %s', check_id, page)
    return IO(result)


def list_check_status(client: Client) -> IO[List[JSON]]:
    result = client.get('/v1/check-statuses')
    LOG.debug('check-status response: %s', result)
    return IO(result)


def list_dashboards(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/dashboards',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('dashboards response: %s', result)
    return IO(result)


def list_env_vars(client: Client, page: PageId) -> IO[List[JSON]]:
    result = []
    try:
        result = client.get(
            '/v1/variables',
            params={'limit': page.per_page, 'page': page.page}
        )
    except HTTPError as error:
        if error.response.status_code != 500:
            raise error
    for item in result:
        item['value'] = '__masked__'
    LOG.debug('variables response: %s', result)
    return IO(result)


def list_mant_windows(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/maintenance-windows',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('maintenance-windows response: %s', result)
    return IO(result)


def list_snippets(client: Client, page: PageId) -> IO[List[JSON]]:
    result = client.get(
        '/v1/snippets',
        params={'limit': page.per_page, 'page': page.page}
    )
    LOG.debug('snippets response: %s', result)
    return IO(result)
