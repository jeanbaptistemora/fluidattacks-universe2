# Standard libraries
import logging
from typing import (
    Optional,
)

# Third party libraries

# Local libraries


LOG = logging.getLogger(__name__)


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
