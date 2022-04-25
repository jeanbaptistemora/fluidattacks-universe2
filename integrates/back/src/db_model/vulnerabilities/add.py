from .types import (
    Vulnerability,
)
from .utils import (
    get_assigned,
    get_zr_index_key,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    VulnAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.constants import (
    ASSIGNED_INDEX_METADATA,
    EVENT_INDEX_METADATA,
    ROOT_INDEX_METADATA,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(  # pylint: disable=too-many-locals
    *, vulnerability: Vulnerability
) -> None:
    items = []
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    gsi_3_index = TABLE.indexes["gsi_3"]
    gsi_4_index = TABLE.indexes["gsi_4"]
    gsi_5_index = TABLE.indexes["gsi_5"]
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(
                vulnerability_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        limit=1,
        table=TABLE,
    )
    if response.items:
        raise VulnAlreadyCreated.new()

    gsi_2_key = keys.build_key(
        facet=ROOT_INDEX_METADATA,
        values={
            "root_id": ""
            if vulnerability.root_id is None
            else vulnerability.root_id,
            "vuln_id": vulnerability.id,
        },
    )
    gsi_3_key = keys.build_key(
        facet=ASSIGNED_INDEX_METADATA,
        values={
            "email": get_assigned(treatment=vulnerability.treatment),
            "vuln_id": vulnerability.id,
        },
    )
    gsi_4_key = keys.build_key(
        facet=EVENT_INDEX_METADATA,
        values={
            "event_id": ""
            if vulnerability.verification is None
            or vulnerability.verification.event_id is None
            else vulnerability.verification.event_id,
            "vuln_id": vulnerability.id,
        },
    )
    gsi_5_key = get_zr_index_key(vulnerability)
    vulnerability_item = {
        key_structure.partition_key: vulnerability_key.partition_key,
        key_structure.sort_key: vulnerability_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_3_index.primary_key.partition_key: gsi_3_key.partition_key,
        gsi_3_index.primary_key.sort_key: gsi_3_key.sort_key,
        gsi_4_index.primary_key.partition_key: gsi_4_key.partition_key,
        gsi_4_index.primary_key.sort_key: gsi_4_key.sort_key,
        gsi_5_index.primary_key.partition_key: gsi_5_key.partition_key,
        gsi_5_index.primary_key.sort_key: gsi_5_key.sort_key,
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

    await operations.batch_put_item(items=tuple(items), table=TABLE)
