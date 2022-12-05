from custom_exceptions import (
    ToeInputNotFound,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputRequest,
    ToeInputState,
)
from freezegun import (
    freeze_time,
)
import pytest
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@freeze_time("2022-11-11T05:00:00+00:00")
async def test_add() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    toe_input = ToeInput(
        attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        attacked_by="test@test.com",
        be_present=True,
        be_present_until=None,
        component="https://test.com/test/new.aspx",
        first_attack_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        entry_point="btnTest",
        group_name=group_name,
        has_vulnerabilities=False,
        seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        seen_first_time_by="new@test.com",
        state=ToeInputState(modified_date="2022-11-11T05:00:00+00:00"),
        unreliable_root_id="",
    )
    await toe_inputs_domain.add(
        loaders=loaders,
        entry_point="btnTest",
        component="https://test.com/test/new.aspx",
        group_name=group_name,
        attributes=ToeInputAttributesToAdd(
            attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
            attacked_by="test@test.com",
            be_present=True,
            has_vulnerabilities=False,
            first_attack_at=datetime.fromisoformat(
                "2021-02-12T05:00:00+00:00"
            ),
            seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
            seen_first_time_by="new@test.com",
            unreliable_root_id="",
        ),
        is_moving_toe_input=True,
    )
    group_toe_inputs = await loaders.group_toe_inputs.clear_all().load_nodes(
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
    assert len(group_toe_inputs) == 6
    current_value = await loaders.toe_input.load(
        ToeInputRequest(
            component="https://test.com/test/new.aspx",
            entry_point="btnTest",
            group_name=group_name,
            root_id="",
        )
    )
    historic_value = await loaders.toe_input_historic.load(
        ToeInputRequest(
            component="https://test.com/test/new.aspx",
            entry_point="btnTest",
            group_name=group_name,
            root_id="",
        )
    )
    assert historic_value == (
        ToeInput(
            attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
            attacked_by="test@test.com",
            be_present=True,
            be_present_until=None,
            component="https://test.com/test/new.aspx",
            entry_point="btnTest",
            first_attack_at=datetime.fromisoformat(
                "2021-02-12T05:00:00+00:00"
            ),
            has_vulnerabilities=False,
            group_name="unittesting",
            seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
            seen_first_time_by="new@test.com",
            unreliable_root_id="",
            state=ToeInputState(modified_date="2022-11-11T05:00:00+00:00"),
        ),
    )

    await toe_inputs_domain.remove(current_value)
    group_toe_inputs = await loaders.group_toe_inputs.clear_all().load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert len(group_toe_inputs) == 5
    with pytest.raises(ToeInputNotFound):
        await loaders.toe_input_historic.clear_all().load(
            ToeInputRequest(
                component="https://test.com/test/new.aspx",
                entry_point="btnTest",
                group_name=group_name,
                root_id="",
            )
        )


@pytest.mark.changes_db
@freeze_time("2022-11-11T15:00:00+00:00")
async def test_update() -> None:
    group_name = "unittesting"
    entry_point = "btnTest"
    component = "https://test.com/test/test.aspx"
    loaders = get_new_context()
    current_value = await loaders.toe_input.load(
        ToeInputRequest(
            component=component,
            entry_point=entry_point,
            group_name=group_name,
            root_id="",
        )
    )
    attributes = ToeInputAttributesToUpdate(
        attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        attacked_by="",
        be_present=True,
        first_attack_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        has_vulnerabilities=False,
        seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        seen_first_time_by="edited@test.com",
        unreliable_root_id="",
    )
    await toe_inputs_domain.update(
        current_value,
        attributes,
        is_moving_toe_input=True,
    )
    loaders = get_new_context()
    toe_input = await loaders.toe_input.load(
        ToeInputRequest(
            component=component,
            entry_point=entry_point,
            group_name=group_name,
            root_id="",
        )
    )
    assert toe_input == ToeInput(
        attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        attacked_by="",
        be_present=True,
        be_present_until=None,
        component="https://test.com/test/test.aspx",
        entry_point="btnTest",
        first_attack_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
        has_vulnerabilities=False,
        group_name=group_name,
        seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        seen_first_time_by="edited@test.com",
        state=ToeInputState(modified_date="2022-11-11T15:00:00+00:00"),
        unreliable_root_id="",
    )
