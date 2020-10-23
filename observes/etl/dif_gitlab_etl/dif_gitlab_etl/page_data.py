# Standard libraries
from os import environ
import tempfile
from typing import (
    Optional,
)
# Third party libraries
import asyncio
# Local libraries
from streamer_gitlab import extractor
from streamer_gitlab.api_client import GitlabResourcePage
from streamer_gitlab.extractor import PageData


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
        extractor.stream_resource_page(
            resource=resource,
            params={},
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
        extractor.stream_resource_page(
            resource=resource,
            params={},
            api_token=api_token,
            out_file=file,
            items_less_than=target_id,
        )
    )
    return result
