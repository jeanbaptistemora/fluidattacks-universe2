from .types import (
    GroupMetadataToUpdate,
    GroupState,
    GroupUnreliableIndicators,
)
from .utils import (
    format_metadata_item,
    format_unreliable_indicators_item,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    GroupNotFound,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.organizations.utils import (
    format_policies_item,
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
    group_name: str,
    metadata: GroupMetadataToUpdate,
    organization_id: str,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={
            "name": group_name,
            "organization_id": remove_org_id_prefix(organization_id),
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
            raise GroupNotFound() from ex


async def update_state(
    *,
    group_name: str,
    organization_id: str,
    state: GroupState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state, default=serialize))
    state_item = {
        key: None if not value and value is not False else value
        for key, value in state_item.items()
        if value is not None
    }

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["group_metadata"],
            values={
                "name": group_name,
                "organization_id": remove_org_id_prefix(organization_id),
            },
        )
        item = {"state": state_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.status").ne(GroupStateStatus.DELETED.value)
        await operations.update_item(
            condition_expression=condition_expression,
            item=item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise GroupNotFound() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["group_historic_state"],
        values={
            "name": group_name,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["group_historic_state"],
        item=historic_item,
        table=TABLE,
    )


async def update_unreliable_indicators(
    *,
    group_name: str,
    indicators: GroupUnreliableIndicators,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        limit=1,
        table=TABLE,
    )
    if not response.items:
        raise GroupNotFound()

    primary_key = keys.build_key(
        facet=TABLE.facets["group_unreliable_indicators"],
        values={
            "name": group_name,
        },
    )
    unreliable_indicators = format_unreliable_indicators_item(indicators)
    await operations.update_item(
        item=unreliable_indicators,
        key=primary_key,
        table=TABLE,
    )


async def update_policies(
    *,
    group_name: str,
    modified_by: str,
    modified_date: datetime,
    organization_id: str,
    policies: PoliciesToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    policies_item = format_policies_item(modified_by, modified_date, policies)

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["group_metadata"],
            values={
                "name": group_name,
                "organization_id": remove_org_id_prefix(organization_id),
            },
        )
        item = {"policies": policies_item}
        condition_expression = Attr(
            key_structure.partition_key
        ).exists() & Attr("state.status").ne(GroupStateStatus.DELETED.value)
        await operations.update_item(
            condition_expression=condition_expression,
            item=item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise GroupNotFound() from ex

    historic_policies_key = keys.build_key(
        facet=TABLE.facets["group_historic_policies"],
        values={
            "name": group_name,
            "iso8601utc": get_as_utc_iso_format(modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_policies_key.partition_key,
        key_structure.sort_key: historic_policies_key.sort_key,
        **policies_item,
    }
    await operations.put_item(
        facet=TABLE.facets["group_historic_policies"],
        item=historic_item,
        table=TABLE,
    )
