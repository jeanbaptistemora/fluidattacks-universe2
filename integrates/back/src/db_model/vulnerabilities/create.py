from .types import (
    Vulnerability,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.utils import (
    format_state_item,
)
from dynamodb import (
    historics,
    keys,
    operations,
)


async def create(*, vulnerability: Vulnerability) -> None:
    items = []
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    vulnerability_metadata = {
        "bug_tracking_system_url": vulnerability.bug_tracking_system_url,
        "commit": vulnerability.commit,
        "custom_severity": vulnerability.custom_severity,
        "finding_id": vulnerability.finding_id,
        "hash": vulnerability.hash,
        "repo": vulnerability.repo,
        "specific": vulnerability.specific,
        "stream": vulnerability.stream,
        "id": vulnerability.id,
        "tags": vulnerability.tags,
        "type": vulnerability.type.value,
        "where": vulnerability.where,
    }
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **vulnerability_metadata,
    }
    items.append(initial_metadata)

    if vulnerability.state:
        historic_state = historics.build_historic(
            attributes=format_state_item(vulnerability.state),
            historic_facet=TABLE.facets["vulnerability_historic_state"],
            key_structure=key_structure,
            key_values={
                "finding_id": vulnerability.finding_id,
                "iso8601utc": vulnerability.state.modified_date,
                "id": vulnerability.id,
            },
            latest_facet=TABLE.facets["vulnerability_state"],
        )
        items.extend(historic_state)

    if vulnerability.treatment:
        historic_treatment = historics.build_historic(
            attributes=dict(vulnerability.treatment._asdict()),
            historic_facet=TABLE.facets["vulnerability_historic_treatment"],
            key_structure=key_structure,
            key_values={
                "finding_id": vulnerability.finding_id,
                "iso8601utc": vulnerability.treatment.modified_date,
                "id": vulnerability.id,
            },
            latest_facet=TABLE.facets["vulnerability_treatment"],
        )
        items.append(historic_treatment)

    if vulnerability.verification:
        historic_verification = historics.build_historic(
            attributes=dict(vulnerability.verification._asdict()),
            historic_facet=TABLE.facets["vulnerability_historic_verification"],
            key_structure=key_structure,
            key_values={
                "finding_id": vulnerability.finding_id,
                "iso8601utc": vulnerability.verification.modified_date,
                "id": vulnerability.id,
            },
            latest_facet=TABLE.facets["vulnerability_verification"],
        )
        items.append(historic_verification)

    if vulnerability.zero_risk:
        historic_zero_risk = historics.build_historic(
            attributes=dict(vulnerability.zero_risk._asdict()),
            historic_facet=TABLE.facets["vulnerability_historic_zero_risk"],
            key_structure=key_structure,
            key_values={
                "finding_id": vulnerability.finding_id,
                "iso8601utc": vulnerability.zero_risk.modified_date,
                "id": vulnerability.id,
            },
            latest_facet=TABLE.facets["vulnerability_zero_risk"],
        )
        items.append(historic_zero_risk)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
