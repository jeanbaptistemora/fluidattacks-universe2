# Standard library
import json
import os

# Local libraries
from backend.dal import (
    analytics as analytics_dal,
)


async def get_document(
    *,
    document_name: str,
    document_type: str,
    level: str,
    subject: str,
) -> str:
    document: str = await analytics_dal.get_document(
        os.path.join(document_type, document_name, f'{level}-{subject}.json')
    )

    return json.loads(document)
