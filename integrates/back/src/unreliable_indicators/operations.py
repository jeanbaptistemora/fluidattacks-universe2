from . import (
    model as unreliable_indicators_model,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicatorsToUpdate,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    Any,
    Set,
)
from unreliable_indicators.enums import (
    EntityAttrName,
    EntityIdName,
    EntityName,
)


async def update_finding_unreliable_indicators(
    context: Any,
    finding_id: str,
    attrs_to_update: Set[EntityAttrName],
) -> None:
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    unreliable_age = None

    if EntityAttrName.unreliable_age in attrs_to_update:
        unreliable_age = await findings_domain.get_finding_age(
            context.loaders, finding.id
        )

    indicators = FindingUnreliableIndicatorsToUpdate(
        unreliable_age=unreliable_age,
    )
    await findings_model.update_unreliable_indicators(
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=indicators,
    )


async def update_unreliable_indicators_by_deps(
    context: Any, dependency: str, **args: str
) -> None:
    entities_to_update = (
        unreliable_indicators_model.get_entities_to_update_by_dependency(
            dependency, **args
        )
    )

    if EntityName.finding in entities_to_update:
        await update_finding_unreliable_indicators(
            context,
            entities_to_update[EntityName.finding].entity_ids[EntityIdName.id],
            entities_to_update[EntityName.finding].attributes_to_update,
        )
