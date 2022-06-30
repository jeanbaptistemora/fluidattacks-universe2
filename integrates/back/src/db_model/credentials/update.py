from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.credentials.types import (
    CredentialNewState,
)
from db_model.credentials.utils import (
    validate_secret,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def update_credential_state_new(
    *,
    current_value: CredentialNewState,
    organization_id: str,
    credential_id: str,
    state: CredentialNewState,
) -> None:
    validate_secret(state)
    key_structure = TABLE.primary_key
    credential_key = keys.build_key(
        facet=TABLE.facets["credentials_new_metadata"],
        values={
            "organization_id": organization_id,
            "id": credential_id,
        },
    )
    state_item = json.loads(json.dumps(state))
    credential_item = {"state": state_item}
    await operations.update_item(
        condition_expression=(
            Attr(key_structure.partition_key).exists()
            & Attr("state.modified_date").eq(current_value.modified_date)
        ),
        item=credential_item,
        key=credential_key,
        table=TABLE,
    )
