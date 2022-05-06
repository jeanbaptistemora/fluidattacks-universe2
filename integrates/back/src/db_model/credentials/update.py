from boto3.dynamodb.conditions import (
    Attr,
)
from datetime import (
    datetime,
    timezone,
)
from db_model import (
    TABLE,
)
from db_model.credentials.types import (
    CredentialState,
)
from dynamodb import (
    historics,
    operations,
)
import simplejson as json  # type: ignore
from typing import (
    Tuple,
)


async def update_credential_state(
    *,
    current_value: CredentialState,
    group_name: str,
    credential_id: str,
    state: CredentialState,
) -> None:
    key_structure = TABLE.primary_key
    latest_facet, historic_facet = (
        TABLE.facets["credentials_state"],
        TABLE.facets["credentials_historic_state"],
    )
    latest, historic = historics.build_historic(
        attributes=json.loads(json.dumps(state)),
        historic_facet=historic_facet,
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": credential_id,
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


async def update_root_ids(
    *,
    current_value: CredentialState,
    modified_by: str,
    group_name: str,
    credential_id: str,
    root_ids: Tuple[str, ...],
) -> None:
    new_state = CredentialState(
        modified_by=modified_by,
        modified_date=datetime.now(tz=timezone.utc).isoformat(),
        name=current_value.name,
        roots=list(root_ids),
        key=current_value.key,
        token=current_value.token,
        user=current_value.user,
        password=current_value.password,
    )
    await update_credential_state(
        current_value=current_value,
        group_name=group_name,
        credential_id=credential_id,
        state=new_state,
    )
