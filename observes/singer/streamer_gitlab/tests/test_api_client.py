# Standard libraries
from os import (
    environ,
)
# Third party libraries
import aiohttp
import pytest
# Local libraries
from streamer_gitlab import api_client
from streamer_gitlab.log import log


@pytest.mark.asyncio
async def test_real_get_json_descending_order():
    api_token = environ['GITLAB_API_TOKEN']
    endpoint = 'https://gitlab.com/api/v4/projects/fluidattacks%2Fservices/jobs'
    result = []
    async with aiohttp.ClientSession() as session:
        result = await api_client.get_json(
            session=session,
            endpoint=endpoint,
            params={
                'page': 1,
                'per_page': 100,
            },
            headers={'Private-Token': api_token},
        )
    last = None
    for item in result:
        if last:
            assert item['id'] < last
            last = item['id']


@pytest.mark.asyncio
async def test_real_get_json_less_than():
    api_token = environ['GITLAB_API_TOKEN']
    endpoint = 'https://gitlab.com/api/v4/projects/fluidattacks%2Fservices/jobs'
    params = {'page': 1, 'per_page': 100,}
    headers = {'Private-Token': api_token}
    result = []
    async with aiohttp.ClientSession() as session:
        pre_result = await api_client.get_json(
            session=session,
            endpoint=endpoint,
            params=params,
            headers=headers,
        )
        result = await api_client.get_json_less_than(
            target_id=pre_result[50]['id'],
            session=session,
            endpoint=endpoint,
            params=params,
            headers=headers,
        )
    assert len(result) <= 50
