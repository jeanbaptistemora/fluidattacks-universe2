# Standard library
from typing import (
    Dict,
    Any
)

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
)
import botocore.exceptions
import rollbar

# Local libraries
from backend.domain import (
    analytics as analytics_domain,
)
from backend.exceptions import DocumentNotFound
from backend.utils import (
    apm,
)


@apm.trace()
@convert_kwargs_to_snake_case
async def resolve(
    *_: Any,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str
) -> Dict[str, object]:
    try:
        return await analytics_domain.get_document(
            document_name=document_name,
            document_type=document_type,
            entity=entity,
            subject=subject,
        )
    except botocore.exceptions.ClientError:
        rollbar.report_exc_info()
        raise DocumentNotFound()
