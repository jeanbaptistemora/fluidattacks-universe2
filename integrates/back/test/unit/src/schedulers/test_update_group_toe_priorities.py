from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
)
import pytest
from schedulers import (
    update_group_toe_priorities,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_update_group_toe_priorities() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "unittesting"
    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name, be_present=True)
    )
    group_sorts_risk_levels = [
        toe_line.state.sorts_risk_level for toe_line in group_toe_lines
    ]
    group_sorts_risk_level_dates = [
        toe_line.state.sorts_risk_level_date for toe_line in group_toe_lines
    ]

    assert group_sorts_risk_levels == [80, 80]
    assert group_sorts_risk_level_dates == [
        datetime(2021, 3, 30, 5, 0, tzinfo=timezone.utc),
        datetime(2021, 2, 20, 5, 0, tzinfo=timezone.utc),
    ]

    await update_group_toe_priorities.main()

    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name, be_present=True)
    )
    group_sorts_risk_levels = [
        toe_line.state.sorts_risk_level for toe_line in group_toe_lines
    ]
    group_sorts_risk_level_dates = [
        toe_line.state.sorts_risk_level_date for toe_line in group_toe_lines
    ]
    current_date = datetime.utcnow().replace(tzinfo=timezone.utc)
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    assert group_sorts_risk_levels == [-1, 1]
    assert group_sorts_risk_level_dates == [
        datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc),
        current_date,
    ]
