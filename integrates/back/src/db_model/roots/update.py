from aioextensions import (
    in_thread,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from context import (
    FI_ENVIRONMENT,
)
from custom_exceptions import (
    IndicatorAlreadyUpdated,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.last_sync import (
    LastUpdateClient,
    operations as last_sync_ops,
    RepoId,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootState,
    IPRootState,
    Root,
    RootUnreliableIndicatorsToUpdate,
    URLRootState,
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
from typing import (
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
    state_item = json.loads(json.dumps(state, default=serialize))

    root_key = keys.build_key(
        facet=metadata_facet,
        values={"name": group_name, "uuid": root_id},
    )
    root_item = {"state": state_item}
    await operations.update_item(
        condition_expression=(
            Attr(key_structure.partition_key).exists()
            & Attr("state.modified_date").eq(
                get_as_utc_iso_format(current_value.modified_date)
            )
        ),
        item=root_item,
        key=root_key,
        table=TABLE,
    )

    historic_key = keys.build_key(
        facet=historic_facet,
        values={
            "uuid": root_id,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
        },
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


async def _update_indicator(repo: RepoId) -> None:
    def _inner() -> None:
        if FI_ENVIRONMENT == "production":
            with last_sync_ops.db_cursor() as cursor:
                client = LastUpdateClient(cursor)
                client.upsert_indicator(repo)

    return await in_thread(_inner)


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    current_value: GitRootCloning,
    repo_nickname: str,
    group_name: str,
    root_id: str,
) -> None:
    key_structure = TABLE.primary_key
    cloning_item = json.loads(json.dumps(cloning, default=serialize))

    root_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
    )
    root_item = {"cloning": cloning_item}
    await operations.update_item(
        condition_expression=(
            Attr(key_structure.partition_key).exists()
            & Attr("cloning.modified_date").eq(
                get_as_utc_iso_format(current_value.modified_date)
            )
        ),
        item=root_item,
        key=root_key,
        table=TABLE,
    )
    if cloning.status is GitCloningStatus.OK:
        await _update_indicator(RepoId(group_name, repo_nickname))
    historic_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_cloning"],
        values={
            "uuid": root_id,
            "iso8601utc": get_as_utc_iso_format(cloning.modified_date),
        },
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
    current_value: Root,
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
        f"unreliable_indicators.{key}": value
        for key, value in json.loads(
            json.dumps(indicators, default=serialize)
        ).items()
        if value is not None
    }
    current_indicators = {
        f"unreliable_indicators.{key}": value
        for key, value in json.loads(
            json.dumps(current_value.unreliable_indicators, default=serialize)
        ).items()
        if value is not None
    }

    conditions = (
        Attr(indicator_name).eq(current_indicators.get(indicator_name))
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
