from dynamodb import (
    model,
)


async def remove_org_finding_policies(*, organization_name: str) -> None:
    await model.remove_org_finding_policies(
        organization_name=organization_name
    )
