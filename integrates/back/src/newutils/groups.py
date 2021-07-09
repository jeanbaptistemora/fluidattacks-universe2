from custom_types import (
    Group as GroupType,
    Historic as HistoricType,
)
import logging
import logging.config
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def has_integrates_services(group: GroupType) -> bool:
    historic_configuration: HistoricType = group.get(
        "historic_configuration", [{}]
    )
    last_config_info = historic_configuration[-1]
    group_has_integrates_services: bool = (
        get_key_or_fallback(last_config_info, "has_squad", "has_drills")
        or last_config_info["has_forces"]
    )

    return group_has_integrates_services
