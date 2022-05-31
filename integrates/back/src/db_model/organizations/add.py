from .types import (
    Organization,
)
from custom_exceptions import (
    OrganizationAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, organization: Organization) -> None:
    # Currently, a prefix could precede the organization id, let's remove it
    organization = organization._replace(
        id=remove_org_id_prefix(organization.id)
    )

    items = []
    key_structure = TABLE.primary_key
    organization_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": organization.id,
            "name": organization.name,
        },
    )

    item_in_db = await operations.get_item(
        facets=(TABLE.facets["organization_metadata"],),
        key=organization_key,
        table=TABLE,
    )
    if item_in_db:
        raise OrganizationAlreadyCreated.new()

    organization_item = {
        key_structure.partition_key: organization_key.partition_key,
        key_structure.sort_key: organization_key.sort_key,
        **json.loads(json.dumps(organization)),
    }
    items.append(organization_item)

    policies_key = keys.build_key(
        facet=TABLE.facets["organization_historic_policies"],
        values={
            "id": organization.id,
            "iso8601utc": organization.policies.modified_date,
        },
    )
    historic_policies_item = {
        key_structure.partition_key: policies_key.partition_key,
        key_structure.sort_key: policies_key.sort_key,
        **json.loads(json.dumps(organization.policies)),
    }
    items.append(historic_policies_item)

    state_key = keys.build_key(
        facet=TABLE.facets["organization_historic_state"],
        values={
            "id": organization.id,
            "iso8601utc": organization.state.modified_date,
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(organization.state)),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
