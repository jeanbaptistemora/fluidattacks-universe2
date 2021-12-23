from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.root_credentials.types import (
    RootCredentialState,
)
from dynamodb import (
    historics,
    operations,
)
import simplejson as json  # type: ignore


async def update_root_credential_state(
    *,
    current_value: RootCredentialState,
    group_name: str,
    root_credential_id: str,
    state: RootCredentialState,
) -> None:
    key_structure = TABLE.primary_key
    latest_facet, historic_facet = (
        TABLE.facets["root_credential_state"],
        TABLE.facets["root_credential_historic_state"],
    )
    latest, historic = historics.build_historic(
        attributes=json.loads(json.dumps(state)),
        historic_facet=historic_facet,
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_credential_id,
        },
        latest_facet=latest_facet,
    )
    await operations.put_item(
        condition_expression=(
            Attr("modified_date").eq(current_value.modified_date)
        ),
        facet=latest_facet,
        item=latest,
        table=TABLE,
    )
    await operations.put_item(facet=historic_facet, item=historic, table=TABLE)
