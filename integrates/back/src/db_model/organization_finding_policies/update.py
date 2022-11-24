from .types import (
    OrgFindingPolicyState,
)
from .utils import (
    serialize_sets,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    OrgFindingPolicyNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json


async def update(
    *,
    organization_name: str,
    finding_policy_id: str,
    state: OrgFindingPolicyState,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={
            "name": organization_name,
            "uuid": finding_policy_id,
        },
    )
    state_item = json.loads(json.dumps(state, default=serialize_sets))
    try:
        item = {"state": state_item}
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise OrgFindingPolicyNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        values={
            "iso8601utc": state.modified_date,
            "uuid": finding_policy_id,
        },
    )
    historic_state_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        item=historic_state_item,
        table=TABLE,
    )
