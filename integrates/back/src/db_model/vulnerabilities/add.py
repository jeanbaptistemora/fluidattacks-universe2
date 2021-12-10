from .types import (
    Vulnerability,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, vulnerability: Vulnerability) -> None:
    items = []
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **json.loads(json.dumps(vulnerability)),
    }
    items.append(initial_metadata)

    state_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={
            "id": vulnerability.id,
            "iso8601utc": vulnerability.state.modified_date,
        },
    )
    historic_state = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(vulnerability.state)),
    }
    items.extend(historic_state)

    if vulnerability.treatment:
        treatment_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_treatment"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.state.modified_date,
            },
        )
        historic_treatment = {
            key_structure.partition_key: treatment_key.partition_key,
            key_structure.sort_key: treatment_key.sort_key,
            **json.loads(json.dumps(vulnerability.treatment)),
        }
        items.append(historic_treatment)

    if vulnerability.verification:
        verification_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_verification"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.state.modified_date,
            },
        )
        historic_verification = {
            key_structure.partition_key: verification_key.partition_key,
            key_structure.sort_key: verification_key.sort_key,
            **json.loads(json.dumps(vulnerability.verification)),
        }
        items.append(historic_verification)

    if vulnerability.zero_risk:
        zero_risk_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_zero_risk"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.state.modified_date,
            },
        )
        historic_zero_risk = {
            key_structure.partition_key: zero_risk_key.partition_key,
            key_structure.sort_key: zero_risk_key.sort_key,
            **json.loads(json.dumps(vulnerability.zero_risk)),
        }
        items.append(historic_zero_risk)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
