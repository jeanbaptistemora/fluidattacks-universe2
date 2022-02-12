from boto3.dynamodb.conditions import (
    Attr,
)
from contextlib import (
    suppress,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootState,
    IPRootState,
    URLRootState,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore
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
            TABLE.facets["git_root_state"],
            TABLE.facets["git_root_historic_state"],
        ),
        IPRootState: (
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["ip_root_historic_state"],
        ),
        URLRootState: (
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
            TABLE.facets["url_root_historic_state"],
        ),
    }
    metadata_facet, latest_facet, historic_facet = root_facets[type(state)]
    state_item = json.loads(json.dumps(state))

    latest, historic = historics.build_historic(
        attributes=state_item,
        historic_facet=historic_facet,
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=latest_facet,
    )
    await operations.put_item(
        condition_expression=(
            Attr("modified_date").eq(current_value.modified_date)
        ),
        facet=latest_facet,
        item=latest,
        table=TABLE,
    )
    root_key = keys.build_key(
        facet=metadata_facet,
        values={"name": group_name, "uuid": root_id},
    )
    root_item = {"state": state_item}
    await operations.update_item(item=root_item, key=root_key, table=TABLE)
    await operations.put_item(facet=historic_facet, item=historic, table=TABLE)


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    current_value: GitRootCloning,
    group_name: str,
    root_id: str,
) -> None:
    key_structure = TABLE.primary_key
    cloning_item = json.loads(json.dumps(cloning))
    latest, historic = historics.build_historic(
        attributes=cloning_item,
        historic_facet=TABLE.facets["git_root_historic_cloning"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": cloning.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_cloning"],
    )
    with suppress(ConditionalCheckFailedException):
        await operations.put_item(
            condition_expression=(
                Attr("modified_date").eq(current_value.modified_date)
            ),
            facet=TABLE.facets["git_root_cloning"],
            item=latest,
            table=TABLE,
        )
        root_key = keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": group_name, "uuid": root_id},
        )
        root_item = {"cloning": cloning_item}
        await operations.update_item(item=root_item, key=root_key, table=TABLE)

        await operations.put_item(
            facet=TABLE.facets["git_root_historic_cloning"],
            item=historic,
            table=TABLE,
        )
