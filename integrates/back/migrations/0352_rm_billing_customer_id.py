# pylint: disable=invalid-name
"""
Remove billing customer id from DB since this id belongs to Stripe test_mode

Execution Time:    2023-01-16 at 17:13:36 UTC
Finalization Time: 2023-01-16 at 17:13:51 UTC

"""

from aioextensions import (
    run,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import os
from settings import (
    LOGGING,
)
import stripe
import time

FI_STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
stripe.api_key = FI_STRIPE_API_KEY
logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_organization(
    org_id: str, org_name: str, customer_id: str
) -> None:
    try:
        data = stripe.Customer.retrieve(customer_id)
        LOGGER_CONSOLE.info(
            "Everything alright with this org!",
            extra=dict(
                extra=dict(
                    org_name=data["name"],
                    created_at=datetime.utcfromtimestamp(data["created"]),
                ),
            ),
        )
    except stripe.error.InvalidRequestError:
        await operations.update_item(
            item={"billing_customer": None},
            key=PrimaryKey(
                partition_key=org_id,
                sort_key=f"ORG#{org_name}",
            ),
            table=TABLE,
        )
        LOGGER_CONSOLE.info(
            "Customer id removed!",
            extra=dict(
                extra=dict(
                    org_name=org_name,
                    org_id=org_id,
                    id_removed=customer_id,
                ),
            ),
        )


async def main() -> None:
    async for organization in orgs_domain.iterate_organizations():
        if organization.billing_customer:
            await process_organization(
                organization.id,
                organization.name,
                organization.billing_customer,
            )
        LOGGER_CONSOLE.info(
            "Org without billing info",
            extra=dict(
                extra=dict(
                    org_name=organization.name,
                    org_id=organization.id,
                ),
            ),
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
