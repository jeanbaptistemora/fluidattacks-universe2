from .types import (
    OrgFindingPolicy,
)
from .utils import (
    serialize_sets,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


async def add(*, policy: OrgFindingPolicy) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={
            "name": policy.organization_name,
            "uuid": policy.id,
        },
    )
    items: list[Item] = []
    metadata_item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(policy, default=serialize_sets)),
    }
    items.append(metadata_item)
    state_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_historic_state"],
        values={
            "iso8601utc": policy.state.modified_date,
            "uuid": policy.id,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(policy.state, default=serialize_sets)),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
