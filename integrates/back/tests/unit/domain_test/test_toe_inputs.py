from dataloaders import (
    get_new_context,
)
from db_model.toe_inputs.types import (
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
        commit="g42343f",
        component="test.com/test/new.aspx",
        created_date="2000-01-01T05:00:00+00:00",
        entry_point="btnTest",
        group_name=group_name,
        seen_first_time_by="new@test.com",
        tested_date="2021-02-12T00:00:00-05:00",
        verified="Yes",
        unreliable_root_id="",
        vulns="New vulns",
    )
    await toe_inputs_domain.add(toe_input)
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert toe_input in group_toe_inputs


@pytest.mark.changes_db
async def test_delete() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert len(group_toe_inputs) == 4
    await toe_inputs_domain.remove(
        entry_point="btnTest",
        component="test.com/test/new.aspx",
        group_name=group_name,
    )
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert len(group_toe_inputs) == 3


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = "unittesting"
    toe_input = ToeInput(
        commit="edited",
        component="test.com/test/test.aspx",
        created_date="2000-01-01T05:00:00+00:00",
        entry_point="btnTest",
        group_name=group_name,
        seen_first_time_by="edited@test.com",
        tested_date="2021-02-12T00:00:00-05:00",
        unreliable_root_id="",
        verified="Yes",
        vulns="Edited vulns",
    )
    await toe_inputs_domain.update(toe_input)
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(group_name)
    assert toe_input in group_toe_inputs
