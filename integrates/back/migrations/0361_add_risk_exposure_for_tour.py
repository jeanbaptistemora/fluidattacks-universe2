# pylint: disable=invalid-name
"""
Add newRiskExposure tour attribute to stakeholders

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders import (
    get_all_stakeholders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    keys,
    operations,
)
import time


async def process_stakeholder(
    stakeholder: Stakeholder, progress: float
) -> None:
    print(f"Working on {stakeholder.email}" f"progress: {round(progress, 2)}")

    stakeholder_tour = stakeholder.tours._asdict() | {
        "new_risk_exposure": False
    }

    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": stakeholder.email,
        },
    )

    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item={"tours": stakeholder_tour},
        key=primary_key,
        table=TABLE,
    )


async def main() -> None:
    all_stakeholders = await get_all_stakeholders()

    print(f"{len(all_stakeholders)=}")
    await collect(
        tuple(
            process_stakeholder(
                stakeholder=stakeholder,
                progress=count / len(all_stakeholders),
            )
            for count, stakeholder in enumerate(all_stakeholders)
        ),
        workers=100,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
