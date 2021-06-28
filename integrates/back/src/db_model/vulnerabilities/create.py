from .metadata import (
    Vulnerability,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    historics,
    keys,
    operations,
)


async def create(*, vulnerability: Vulnerability) -> None:  # noqa: MC0001
    items = []
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "uuid": vulnerability.uuid,
        },
    )
    vulnerability_metadata = {
        "finding_id": vulnerability.finding_id,
        "source": vulnerability.source.value,
        "specific": vulnerability.specific,
        "uuid": vulnerability.uuid,
        "type": vulnerability.type.value,
        "where": vulnerability.where,
    }
    if vulnerability.bts_url:
        vulnerability_metadata["bts_url"] = vulnerability.bts_url
    if vulnerability.commit:
        vulnerability_metadata["commit"] = vulnerability.commit
    if vulnerability.custom_severity:
        vulnerability_metadata[
            "custom_severity"
        ] = vulnerability.custom_severity
    if vulnerability.hash:
        vulnerability_metadata["hash"] = vulnerability.hash
    if vulnerability.repo:
        vulnerability_metadata["repo"] = vulnerability.repo
    if vulnerability.stream:
        vulnerability_metadata["stream"] = vulnerability.stream
    if vulnerability.tags:
        vulnerability_metadata["tags"] = vulnerability.tags
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **vulnerability_metadata,
    }
    items.append(initial_metadata)

    historic_state = historics.build_historic(
        attributes=dict(vulnerability.state._asdict()),
        historic_facet=TABLE.facets["vulnerability_historic_state"],
        key_structure=key_structure,
        key_values={
            "finding_id": vulnerability.finding_id,
            "iso8601utc": vulnerability.state.modified_date,
            "uuid": vulnerability.uuid,
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
                "uuid": vulnerability.uuid,
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
                "uuid": vulnerability.uuid,
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
                "uuid": vulnerability.uuid,
            },
            latest_facet=TABLE.facets["vulnerability_zero_risk"],
        )
        items.append(historic_zero_risk)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
