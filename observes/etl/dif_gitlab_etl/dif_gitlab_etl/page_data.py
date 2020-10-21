# Standard libraries
from os import environ
import tempfile
from typing import (
    Optional,
)
# Third party libraries
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
    file = tempfile.TemporaryFile()
    return extractor.stream_resource_page(
        resource=resource,
        params={},
        api_token=api_token,
        out_file=file,
    )


def extract_data_less_than(
    target_id: int,
    resource: GitlabResourcePage,
) -> Optional[PageData]:
    """
    Returns the PageData of the resource.
    The PageData.file stores the retrieved data.
    """
    api_token = environ['GITLAB_API_TOKEN']
    file = tempfile.TemporaryFile()
    return extractor.stream_resource_page(
        resource=resource,
        params={},
        api_token=api_token,
        out_file=file,
        items_less_than=target_id,
    )
