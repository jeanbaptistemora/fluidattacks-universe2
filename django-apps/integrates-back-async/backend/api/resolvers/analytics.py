# Standard library
from typing import (
    Dict,
    Any,
    cast
)

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
)
import botocore.exceptions

# Local libraries
from backend.domain import (
    analytics as analytics_domain,
)
from backend.exceptions import DocumentNotFound
from backend.utils import (
    apm,
    logging as logging_utils,
)


@apm.trace()
@convert_kwargs_to_snake_case  # type: ignore
async def resolve(
    *_: Any,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str
) -> Dict[str, Any]:
    try:
        return cast(
            Dict[str, Any],
            await analytics_domain.get_document(
                document_name=document_name,
                document_type=document_type,
                entity=entity,
                subject=subject,
            )
        )
    except botocore.exceptions.ClientError as ex:
        await logging_utils.log(ex, 'error', extra=locals())
        raise DocumentNotFound()
