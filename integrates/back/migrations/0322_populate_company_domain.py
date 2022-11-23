# pylint: disable=invalid-name
"""
Populates gsi2 with the domain name of the company,
which will be used to validate trial uniqueness per company

Execution Time:
Finalization Time:
"""
from aioextensions import (
    collect,
    run,
)
from db_model import (
    stakeholders as stakeholders_model,
    TABLE,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import time


async def process_stakeholder(email: str) -> None:
    domain_name = email.split("@")[1]
    company = domain_name.split(".")[0]

    await operations.update_item(
        item={"pk_2": f"CO#{company}", "sk_2": f"ENROLL#{email}"},
        key=PrimaryKey(
            partition_key=f"ENROLL#{email}", sort_key=f"ENROLL#{email}"
        ),
        table=TABLE,
    )


async def main() -> None:
    all_stakeholders = await stakeholders_model.get_all_stakeholders()
    await collect(
        tuple(
            process_stakeholder(stakeholder.email)
            for stakeholder in all_stakeholders
        ),
        workers=100,
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
