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
    operations,
)
import simplejson as json  # type: ignore
from typing import (
    Union,
)


async def update_root_state(
    *,
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=json.loads(json.dumps(state)),
        historic_facet=TABLE.facets["git_root_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_state"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def update_git_root_cloning(
    *, cloning: GitRootCloning, group_name: str, root_id: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(cloning._asdict()),
        historic_facet=TABLE.facets["git_root_historic_cloning"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": cloning.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_cloning"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)
