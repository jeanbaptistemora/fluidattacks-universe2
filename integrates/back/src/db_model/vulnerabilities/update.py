from .historics.state import (
    format_state_item,
    VulnerabilityState,
)
from .historics.treatment import (
    format_treatment_item,
    VulnerabilityTreatment,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    historics,
    operations,
)


async def update_state(
    *,
    finding_id: str,
    state: VulnerabilityState,
    uuid: str,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    state_item = format_state_item(state)
    latest, historic = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets["vulnerability_historic_state"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": state.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_state"],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=TABLE.facets["vulnerability_state"],
        item=latest,
        table=TABLE,
    )
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_treatment(
    *,
    finding_id: str,
    treatment: VulnerabilityTreatment,
    uuid: str,
) -> None:
    items = []
    key_structure = TABLE.primary_key
    treatment_item = format_treatment_item(treatment)
    latest, historic = historics.build_historic(
        attributes=treatment_item,
        historic_facet=TABLE.facets["vulnerability_historic_treatment"],
        key_structure=key_structure,
        key_values={
            "finding_id": finding_id,
            "iso8601utc": treatment.modified_date,
            "uuid": uuid,
        },
        latest_facet=TABLE.facets["vulnerability_treatment"],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=TABLE.facets["vulnerability_treatment"],
        item=latest,
        table=TABLE,
    )
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)
