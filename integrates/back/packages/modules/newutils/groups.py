# Standard libraries
import logging
import logging.config

# Third-party libraries

# Local libraries
from back.settings import LOGGING
from backend.typing import (
    Historic as HistoricType,
    Project as ProjectType,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def has_integrates_services(group: ProjectType) -> bool:
    historic_configuration: HistoricType = (
        group.get('historic_configuration', [{}])
    )
    last_config_info = historic_configuration[-1]
    group_has_integrates_services: bool = (
        last_config_info['has_drills']
        or last_config_info['has_forces']
    )

    return group_has_integrates_services
