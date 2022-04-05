from boto3.dynamodb.conditions import (
    Attr,
)
import botocore
from contextlib import (
    suppress,
)
from custom_exceptions import (
    IndicatorAlreadyUpdated,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootState,
    IPRootState,
    MachineFindingResult,
    RootItem,
    RootUnreliableIndicatorsToUpdate,
    URLRootState,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore
from typing import (
    List,
    Union,
)


async def update_root_state(
    *,
    current_value: Union[GitRootState, IPRootState, URLRootState],
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    key_structure = TABLE.primary_key
    root_facets = {
        GitRootState: (
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_historic_state"],
        ),
        IPRootState: (
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_historic_state"],
        ),
        URLRootState: (
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_historic_state"],
        ),
    }
    metadata_facet, historic_facet = root_facets[type(state)]
    state_item = json.loads(json.dumps(state))

    root_key = keys.build_key(
        facet=metadata_facet,
        values={"name": group_name, "uuid": root_id},
    )
    root_item = {"state": state_item}
    await operations.update_item(
        condition_expression=(
            Attr(key_structure.partition_key).exists()
            & Attr("state.modified_date").eq(current_value.modified_date)
        ),
        item=root_item,
        key=root_key,
        table=TABLE,
    )

    historic_key = keys.build_key(
        facet=historic_facet,
        values={"uuid": root_id, "iso8601utc": state.modified_date},
    )
    historic_item = {
        key_structure.partition_key: historic_key.partition_key,
        key_structure.sort_key: historic_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=historic_facet,
        item=historic_item,
        table=TABLE,
    )


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    current_value: GitRootCloning,
    group_name: str,
    root_id: str,
) -> None:
    key_structure = TABLE.primary_key
    cloning_item = json.loads(json.dumps(cloning))

    with suppress(ConditionalCheckFailedException):
        root_key = keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": group_name, "uuid": root_id},
        )
        root_item = {"cloning": cloning_item}
        await operations.update_item(
            condition_expression=(
                Attr(key_structure.partition_key).exists()
                & Attr("cloning.modified_date").eq(current_value.modified_date)
            ),
            item=root_item,
            key=root_key,
            table=TABLE,
        )

        historic_key = keys.build_key(
            facet=TABLE.facets["git_root_historic_cloning"],
            values={"uuid": root_id, "iso8601utc": cloning.modified_date},
        )
        historic_item = {
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
            **cloning_item,
        }
        await operations.put_item(
            facet=TABLE.facets["git_root_historic_cloning"],
            item=historic_item,
            table=TABLE,
        )


async def update_unreliable_indicators(
    *,
    current_value: RootItem,
    indicators: RootUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    root_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={
            "name": current_value.group_name,
            "uuid": current_value.id,
        },
    )

    unreliable_indicators = {
        f"unreliable_indicators.{key}": (
            Decimal(str(value)) if isinstance(value, float) else value
        )
        for key, value in json.loads(json.dumps(indicators)).items()
        if value is not None
    }
    current_indicators = {
        f"unreliable_indicators.{key}": (
            Decimal(str(value)) if isinstance(value, float) else value
        )
        for key, value in json.loads(
            json.dumps(current_value.unreliable_indicators)
        ).items()
        if value is not None
    }

    conditions = (
        Attr(indicator_name).not_exists()
        | Attr(indicator_name).eq(current_indicators[indicator_name])
        for indicator_name in unreliable_indicators
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition

    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=unreliable_indicators,
            key=root_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex


async def finish_machine_execution(
    root_id: str,
    job_id: str,
    stopped_at: str,
    findings_executed: List[MachineFindingResult],
) -> bool:
    key_structure = TABLE.primary_key
    machine_execution_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution"],
        values={"uuid": root_id, "job_id": job_id},
    )

    with suppress(botocore.exceptions.ClientError):
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item={
                "stopped_at": stopped_at,
                "findings_executed": findings_executed,
            },
            key=machine_execution_key,
            table=TABLE,
        )
        return True

    return False


async def remove_secret(root_id: str, secret_key: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_secret"],
        values={"uuid": root_id, "key": secret_key},
    )
    await operations.delete_item(key=primary_key, table=TABLE)
