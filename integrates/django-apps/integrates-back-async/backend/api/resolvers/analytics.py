# Standard library
import logging
from typing import (
    Dict,
    Any,
    cast
)

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
)

# Local libraries
from backend.domain import (
    analytics as analytics_domain,
)
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
async def resolve(
    *_: Any,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str
) -> Dict[str, Any]:
    return cast(
        Dict[str, Any],
        await analytics_domain.get_document(
            document_name=document_name,
            document_type=document_type,
            entity=entity,
            subject=subject,
        )
    )
