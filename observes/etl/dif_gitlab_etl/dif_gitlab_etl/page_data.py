# Standard libraries
from typing import (
    Optional,
    NamedTuple,
)
# Third party libraries
# Local libraries
from streamer_gitlab.api_client import GitlabResourcePage


class PageData(NamedTuple):
    id: int
    path: str
    minor_item_id: int


# temporal interface definition
def extract_data(
    resource: GitlabResourcePage  # pylint: disable=unused-argument
) -> Optional[PageData]:
    """
    Returns the PageData of the resource.
    The PageData.path stores the retrieved data.
    """


# temporal interface definition
def extract_data_less_than(
    target_id: int,  # pylint: disable=unused-argument
    resource: GitlabResourcePage  # pylint: disable=unused-argument
) -> Optional[PageData]:
    """
    Returns the PageData of the resource.
    The PageData.path stores the retrieved data.
    """
