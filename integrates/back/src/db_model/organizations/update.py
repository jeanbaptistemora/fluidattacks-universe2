from .types import (
    OrganizationMetadataToUpdate,
    OrganizationState,
)
from .utils import (
    format_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    OrganizationNotFound,
)
from db_model import (
    TABLE,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def update_metadata(
    *,
    metadata: OrganizationMetadataToUpdate,
    organization_id: str,
    organization_name: str,
) -> None:
    key_structure = TABLE.primary_key
    organization_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": remove_org_id_prefix(organization_id),
            "name": organization_name,
        },
    )
    organization_item = format_metadata_item(metadata)
    if organization_item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=organization_item,
                key=organization_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise OrganizationNotFound() from ex


async def update_state(
    *,
    organization_id: str,
    organization_name: str,
    state: OrganizationState,
) -> None:
    organization_id = remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state))
    state_item = {
        key: None if not value and value is not False else value
        for key, value in state_item.items()
        if value is not None
    }

    try:
        organization_key = keys.build_key(
            facet=TABLE.facets["organization_metadata"],
            values={
                "id": organization_id,
                "name": organization_name,
            },
        )
        organization_item = {"state": state_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.status").ne(
            OrganizationStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=condition_expression,
            item=organization_item,
            key=organization_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise OrganizationNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["organization_historic_state"],
        values={
            "id": organization_id,
            "iso8601utc": state.modified_date,
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["organization_historic_state"],
        item=historic_item,
        table=TABLE,
    )
