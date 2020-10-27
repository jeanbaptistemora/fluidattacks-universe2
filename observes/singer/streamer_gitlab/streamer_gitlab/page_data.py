# Standard libraries
from os import environ
import sys
import tempfile
from typing import (
    cast,
    IO,
    NamedTuple,
    Optional,
    TextIO,
)
# Third party libraries
import asyncio
from asyncio import (
    Queue
)
import urllib.parse
# Local libraries
from streamer_gitlab import api_client
from streamer_gitlab import extractor
from streamer_gitlab.api_client import GitlabResourcePage


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


async def stream_resource_page(
    resource: GitlabResourcePage,
    api_token: str,
    out_file: IO[str] = sys.stdout,
    items_less_than: Optional[int] = None,
) -> Optional[PageData]:
    sys.stdout = cast(TextIO, out_file)
    project: str = resource.g_resource.project
    s_resource: str = resource.g_resource.resource
    init_page: int = resource.page
    per_page: int = resource.per_page
    queue: Queue = Queue(maxsize=1024)
    await extractor.collect([
        extractor.gitlab_data_emitter(
            api_client.build_getter(items_less_than),
            urllib.parse.quote(project, safe=''),
            s_resource,
            dict(resource.g_resource.params),
            api_token,
            1, per_page, init_page
        )(queue)
    ])
    m_id: Optional[int] = None
    if queue.qsize() > 0:
        item = await queue.get()
        m_id = api_client.get_minor_id(item['records'])
        if m_id is not None:
            await queue.put(item)
            await queue.put(None)
            await extractor.create_task(extractor.emitter(queue))
            return PageData(
                resource,
                file=out_file,
                minor_item_id=m_id
            )
    out_file.close()
    return None
