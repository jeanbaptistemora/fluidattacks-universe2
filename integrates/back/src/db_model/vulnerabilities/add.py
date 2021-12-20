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

    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    vulnerability_item = {
        key_structure.partition_key: vulnerability_key.partition_key,
        key_structure.sort_key: vulnerability_key.sort_key,
        **json.loads(json.dumps(vulnerability)),
    }
    items.append(vulnerability_item)

    state_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={
            "id": vulnerability.id,
            "iso8601utc": vulnerability.state.modified_date,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(vulnerability.state)),
    }
    items.append(historic_state_item)

    if vulnerability.treatment:
        treatment_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_treatment"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.treatment.modified_date,
            },
        )
        historic_treatment_item = {
            key_structure.partition_key: treatment_key.partition_key,
            key_structure.sort_key: treatment_key.sort_key,
            **json.loads(json.dumps(vulnerability.treatment)),
        }
        items.append(historic_treatment_item)

    if vulnerability.verification:
        verification_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_verification"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.verification.modified_date,
            },
        )
        historic_verification_item = {
            key_structure.partition_key: verification_key.partition_key,
            key_structure.sort_key: verification_key.sort_key,
            **json.loads(json.dumps(vulnerability.verification)),
        }
        items.append(historic_verification_item)

    if vulnerability.zero_risk:
        zero_risk_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_zero_risk"],
            values={
                "id": vulnerability.id,
                "iso8601utc": vulnerability.zero_risk.modified_date,
            },
        )
        historic_zero_risk_item = {
            key_structure.partition_key: zero_risk_key.partition_key,
            key_structure.sort_key: zero_risk_key.sort_key,
            **json.loads(json.dumps(vulnerability.zero_risk)),
        }
        items.append(historic_zero_risk_item)

    await operations.batch_write_item(items=tuple(items), table=TABLE)
