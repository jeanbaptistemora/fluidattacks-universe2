from db_model import (
    companies as companies_model,
)
from db_model.companies.types import (
    CompanyMetadataToUpdate,
)


async def update_metadata(
    domain: str,
    metadata: CompanyMetadataToUpdate,
) -> None:
    await companies_model.update_metadata(
        domain=domain,
        metadata=metadata,
    )
