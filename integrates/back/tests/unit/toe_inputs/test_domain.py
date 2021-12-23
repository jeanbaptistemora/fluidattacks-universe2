from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
)
import pytest
from toe.inputs import (
    domain as toe_inputs_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add() -> None:
    group_name = "unittesting"
    toe_input = ToeInput(
        attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        attacked_by="test@test.com",
        be_present=True,
        be_present_until=None,
        component="test.com/test/new.aspx",
        first_attack_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        entry_point="btnTest",
        group_name=group_name,
        seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        seen_first_time_by="new@test.com",
        unreliable_root_id="",
    )
    await toe_inputs_domain.add(toe_input)
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert toe_input in group_toe_inputs


@pytest.mark.changes_db
async def test_delete() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert len(group_toe_inputs) == 4
    await toe_inputs_domain.remove(
        entry_point="btnTest",
        component="test.com/test/new.aspx",
        group_name=group_name,
    )
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert len(group_toe_inputs) == 3


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = "unittesting"
    toe_input = ToeInput(
        attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        attacked_by="",
        be_present=True,
        be_present_until=None,
        component="test.com/test/test.aspx",
        entry_point="btnTest",
        first_attack_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        group_name=group_name,
        seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        seen_first_time_by="edited@test.com",
        unreliable_root_id="",
    )
    await toe_inputs_domain.update(toe_input)
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert toe_input in group_toe_inputs
