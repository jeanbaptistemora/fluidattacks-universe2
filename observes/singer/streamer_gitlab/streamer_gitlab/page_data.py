# Standard libraries
import json
from os import environ
import sys
import tempfile
from typing import (
    Any,
    Dict,
    IO,
    List,
    NamedTuple,
    Optional,
)
# Third party libraries
import asyncio
import aiohttp
# Local libraries
from streamer_gitlab import api_client
from streamer_gitlab import extractor
from streamer_gitlab.api_client import GitlabResourcePage
from streamer_gitlab.log import log


class PageData(NamedTuple):
    id: GitlabResourcePage
    file: IO[str]
    minor_item_id: int


def extract_data(
    resource: GitlabResourcePage,
) -> Optional[PageData]:
    """
    Returns the PageData of the resource.
    The PageData.file stores the retrieved data.
    """
    api_token = environ['GITLAB_API_TOKEN']
    file = tempfile.NamedTemporaryFile(mode='w+')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        stream_resource_page(
            resource=resource,
            api_token=api_token,
            out_file=file,
        )
    )
    return result


def extract_data_less_than(
    target_id: int,
    resource: GitlabResourcePage,
) -> Optional[PageData]:
    """
    Returns the PageData of the resource.
    The PageData.file stores the retrieved data.
    """
    api_token = environ['GITLAB_API_TOKEN']
    file = tempfile.NamedTemporaryFile(mode='w+')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        stream_resource_page(
            resource=resource,
            api_token=api_token,
            out_file=file,
            items_less_than=target_id,
        )
    )
    return result


def filter_data_greater_than(
    target_id: int,
    dpage: PageData
) -> Optional[PageData]:
    """
    Returns a PageData only with items greater than target_id
    """
    dpage.file.seek(0)
    log('debug', f'Filter greater than @ {dpage.file.name}')
    lines = dpage.file.readlines()
    data: List[Dict[str, Any]] = []
    stream = ''
    for line in lines:
        raw_data: Dict[str, Any] = json.loads(line)
        if not stream:
            stream = raw_data['stream']
        elif stream != raw_data['stream']:
            raise Exception(
                'PageData is expected to hold items with same stream property'
            )
        data.append(raw_data['record'])
    filtered_records = api_client.elements_greater_than(
        target_id, data
    )
    file = tempfile.NamedTemporaryFile(mode='w+')
    extractor.emit(stream, filtered_records, file)
    return PageData(
        id=dpage.id,
        file=file,
        minor_item_id=dpage.minor_item_id
    )


async def stream_resource_page(
    resource: GitlabResourcePage,
    api_token: str,
    out_file: IO[str] = sys.stdout,
    items_less_than: Optional[int] = None,
) -> Optional[PageData]:
    """
    Rerieves remote data of a target resource and
    creates a PageData object using the supplied file
    """
    async with aiohttp.ClientSession() as session:
        result: List[Dict[str, Any]] = await api_client.get_resource(
            session, resource, items_less_than,
            headers={'Private-Token': api_token}
        )
        m_id: Optional[int] = None
        m_id = api_client.get_minor_id(result)
        if m_id is not None:
            extractor.emit(resource.g_resource.resource, result, out_file)
            return PageData(
                resource,
                file=out_file,
                minor_item_id=m_id
            )
        out_file.close()
        return None
