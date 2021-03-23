# Standard libraries
from typing import (
    Optional,
)

# Third party libraries

# Local libraries
import utils_logger

LOG = utils_logger.get_log(__name__)


def list_items_alert(ref: str, total: Optional[int]) -> None:
    max_items = 1000
    if total is None:
        LOG.error('total_items is missing at `%s`', ref)
    elif total > max_items:
        LOG.error(
            'Data at `%s` suprassed max handled items (%s > max_items)',
            ref,
            total
        )
