from .types import (
    OrganizationMetadataToUpdate,
    OrganizationState,
    OrganizationUnreliableIndicators,
    OrganizationUnreliableIndicatorsToUpdate,
)
from .utils import (
    format_metadata_item,
    format_policies_item,
    format_unreliable_indicators_item,
    format_unreliable_indicators_item_to_update,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    OrganizationNotFound,
)
from datetime import (
    datetime,
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
from db_model.types import (
    PoliciesToUpdate,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json


async def update_metadata(
    *,
    metadata: OrganizationMetadataToUpdate,
    organization_id: str,
    organization_name: str,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": remove_org_id_prefix(organization_id),
            "name": organization_name,
        },
    )
    item = format_metadata_item(metadata)
    if item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=item,
                key=primary_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise OrganizationNotFound() from ex


async def update_policies(
    *,
    modified_by: str,
    modified_date: datetime,
    organization_id: str,
    organization_name: str,
    policies: PoliciesToUpdate,
) -> None:
    organization_id = remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    policies_item = format_policies_item(modified_by, modified_date, policies)

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["organization_metadata"],
            values={
                "id": organization_id,
                "name": organization_name,
            },
        )
        organization_item = {"policies": policies_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.status").ne(
            OrganizationStateStatus.DELETED.value
        )
        await operations.update_item(
            condition_expression=condition_expression,
            item=organization_item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise OrganizationNotFound() from ex

    historic_policies_key = keys.build_key(
        facet=TABLE.facets["organization_historic_policies"],
        values={
            "id": organization_id,
            "iso8601utc": get_as_utc_iso_format(modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_policies_key.partition_key,
        key_structure.sort_key: historic_policies_key.sort_key,
        **policies_item,
    }
    await operations.put_item(
        facet=TABLE.facets["organization_historic_policies"],
        item=historic_item,
        table=TABLE,
    )


async def update_state(
    *,
    organization_id: str,
    organization_name: str,
    state: OrganizationState,
) -> None:
    organization_id = remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state, default=serialize))
    state_item = {
        key: None if not value else value
        for key, value in state_item.items()
        if value is not None
    }

    try:
        primary_key = keys.build_key(
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
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise OrganizationNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["organization_historic_state"],
        values={
            "id": organization_id,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
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


async def update_unreliable_indicators(
    *,
    organization_id: str,
    organization_name: str,
    indicators: OrganizationUnreliableIndicators,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={
            "id": organization_id,
            "name": organization_name,
        },
    )
    unreliable_indicators = format_unreliable_indicators_item(indicators)
    await operations.update_item(
        item=unreliable_indicators,
        key=primary_key,
        table=TABLE,
    )


async def update_unreliable_org_indicators(
    *,
    organization_id: str,
    organization_name: str,
    indicators: OrganizationUnreliableIndicatorsToUpdate,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={
            "id": organization_id,
            "name": organization_name,
        },
    )
    unreliable_indicators = format_unreliable_indicators_item_to_update(
        indicators
    )

    await operations.update_item(
        item=unreliable_indicators,
        key=primary_key,
        table=TABLE,
    )
