from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
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
    ToeInputMetadataToUpdate,
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
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "component",
        "entry_point",
        "attributes",
        "is_moving_toe_input",
    ],
    [
        [
            "unittesting",
            "https://test.com/test/new.aspx",
            "btnTest",
            ToeInputAttributesToAdd(
                attacked_at=datetime.fromisoformat(
                    "2021-02-12T05:00:00+00:00"
                ),
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
            True,
        ],
    ],
)
@freeze_time("2022-11-11T05:00:00+00:00")
async def test_add(
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
    is_moving_toe_input: bool,
) -> None:
    loaders = get_new_context()
    toe_input = ToeInput(
        component="https://test.com/test/new.aspx",
        entry_point="btnTest",
        group_name=group_name,
        state=ToeInputState(
            attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
            attacked_by="test@test.com",
            be_present=True,
            be_present_until=None,
            first_attack_at=datetime.fromisoformat(
                "2021-02-12T05:00:00+00:00"
            ),
            has_vulnerabilities=False,
            modified_by="new@test.com",
            modified_date=datetime.fromisoformat("2022-11-11T05:00:00+00:00"),
            seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
            seen_first_time_by="new@test.com",
            unreliable_root_id="",
        ),
    )
    await toe_inputs_domain.add(
        loaders=loaders,
        entry_point=entry_point,
        component=component,
        group_name=group_name,
        attributes=attributes,
        is_moving_toe_input=is_moving_toe_input,
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
    assert len(group_toe_inputs) == 5
    current_value = await loaders.toe_input.load(
        ToeInputRequest(
            component="https://test.com/test/new.aspx",
            entry_point="btnTest",
            group_name=group_name,
            root_id="",
        )
    )
    assert current_value
    historic_value = await loaders.toe_input_historic.load(
        ToeInputRequest(
            component="https://test.com/test/new.aspx",
            entry_point="btnTest",
            group_name=group_name,
            root_id="",
        )
    )
    if historic_value:
        assert historic_value == [
            ToeInput(
                component="https://test.com/test/new.aspx",
                entry_point="btnTest",
                group_name="unittesting",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-12T05:00:00+00:00"
                    ),
                    attacked_by="test@test.com",
                    be_present=True,
                    be_present_until=None,
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-12T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="new@test.com",
                    modified_date=datetime.fromisoformat(
                        "2022-11-11T05:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    ),
                    seen_first_time_by="new@test.com",
                    unreliable_root_id="",
                ),
            ),
        ]

    await toe_inputs_domain.remove(current_value)
    group_toe_inputs = await loaders.group_toe_inputs.clear_all().load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert len(group_toe_inputs) == 4
    if not historic_value:
        await loaders.toe_input_historic.clear_all().load(
            ToeInputRequest(
                component="https://test.com/test/new.aspx",
                entry_point="btnTest",
                group_name=group_name,
                root_id="",
            )
        )


@pytest.mark.parametrize(
    [
        "current_value",
        "attributes",
        "modified_by",
        "is_moving_toe_input",
    ],
    [
        [
            ToeInput(
                component="https://test.com/test/test.aspx",
                entry_point="btnTest",
                group_name="unittesting",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
                    attacked_by="test@test.com",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-20T15:41:04+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2021-01-02T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="test2@test.com",
                    modified_date=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-03-14T05:00:00+00:00"
                    ),
                    seen_first_time_by="test@test.com",
                    unreliable_root_id="",
                ),
            ),
            ToeInputAttributesToUpdate(
                attacked_at=datetime.fromisoformat(
                    "2021-02-12T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                first_attack_at=datetime.fromisoformat(
                    "2021-02-12T05:00:00+00:00"
                ),
                has_vulnerabilities=False,
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="edited@test.com",
                unreliable_root_id="",
            ),
            "edited@test.com",
            True,
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "toe_inputs_model.update_state", new_callable=AsyncMock
)
@freeze_time("2022-11-11T15:00:00+00:00")
async def test_update(
    mock_toe_inputs_model_update_state: AsyncMock,
    current_value: ToeInput,
    attributes: ToeInputAttributesToUpdate,
    modified_by: str,
    is_moving_toe_input: bool,
) -> None:

    assert set_mocks_return_values(
        mocks_args=[[current_value, attributes, modified_by]],
        mocked_objects=[mock_toe_inputs_model_update_state],
        module_at_test=MODULE_AT_TEST,
        paths_list=["toe_inputs_model.update_state"],
    )

    await toe_inputs_domain.update(
        current_value=current_value,
        attributes=attributes,
        modified_by=modified_by,
        is_moving_toe_input=is_moving_toe_input,
    )

    mock_toe_inputs_model_update_state.assert_called_with(
        current_value=current_value,
        new_state=ToeInputState(
            attacked_at=datetime.fromisoformat("2021-02-12T05:00:00+00:00"),
            attacked_by="",
            be_present=True,
            be_present_until=None,
            first_attack_at=datetime.fromisoformat(
                "2021-02-12T05:00:00+00:00"
            ),
            has_vulnerabilities=False,
            modified_by="edited@test.com",
            modified_date=datetime.fromisoformat("2022-11-11T15:00:00+00:00"),
            seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
            seen_first_time_by="edited@test.com",
            unreliable_root_id="",
        ),
        metadata=ToeInputMetadataToUpdate(
            clean_attacked_at=False,
            clean_be_present_until=True,
            clean_first_attack_at=False,
            clean_seen_at=False,
        ),
    )
