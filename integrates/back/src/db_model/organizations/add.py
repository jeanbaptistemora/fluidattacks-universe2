from .types import (
    Organization,
)
from custom_exceptions import (
    OrganizationAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.organizations.constants import (
    ALL_ORGANIZATIONS_INDEX_METADATA,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json


async def add(*, organization: Organization) -> None:
    # Currently, a prefix could precede the organization id, let's remove it
    organization = organization._replace(
        id=remove_org_id_prefix(organization.id)
    )

    items = []
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": organization.id,
            "name": organization.name,
        },
    )

    item_in_db = await operations.get_item(
        facets=(TABLE.facets["organization_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if item_in_db:
        raise OrganizationAlreadyCreated.new()

    gsi_2_key = keys.build_key(
        facet=ALL_ORGANIZATIONS_INDEX_METADATA,
        values={
            "all": "all",
            "id": organization.id,
        },
    )

    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **json.loads(json.dumps(organization, default=serialize)),
    }
    items.append(item)

    policies_key = keys.build_key(
        facet=TABLE.facets["organization_historic_policies"],
        values={
            "id": organization.id,
            "iso8601utc": get_as_utc_iso_format(
                organization.policies.modified_date
            ),
        },
    )
    historic_policies_item = {
        key_structure.partition_key: policies_key.partition_key,
        key_structure.sort_key: policies_key.sort_key,
        **json.loads(json.dumps(organization.policies, default=serialize)),
    }
    items.append(historic_policies_item)

    state_key = keys.build_key(
        facet=TABLE.facets["organization_historic_state"],
        values={
            "id": organization.id,
            "iso8601utc": get_as_utc_iso_format(
                organization.state.modified_date
            ),
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(organization.state, default=serialize)),
    }
    items.append(historic_state_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
