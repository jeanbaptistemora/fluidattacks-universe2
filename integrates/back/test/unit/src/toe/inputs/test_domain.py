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
    ToeInput,
    ToeInputMetadataToUpdate,
    ToeInputState,
)
from freezegun import (
    freeze_time,
)
import pytest
from toe.inputs.domain import (
    add,
    remove,
    update,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)
from typing import (
    Any,
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
                unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            ),
            False,
        ],
    ],
)
@patch(MODULE_AT_TEST + "toe_inputs_model.add", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "validate_component", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "roots_domain.get_root", new_callable=AsyncMock)
@freeze_time("2022-11-11T05:00:00+00:00")
async def test_add(  # pylint: disable=too-many-arguments
    mock_roots_domain_get_root: AsyncMock,
    mock_validate_component: AsyncMock,
    mock_toe_inputs_model_add: AsyncMock,
    group_name: str,
    component: str,
    entry_point: str,
    attributes: ToeInputAttributesToAdd,
    is_moving_toe_input: bool,
) -> None:
    if is_moving_toe_input:
        assert set_mocks_return_values(
            mocks_args=[[group_name, component, entry_point, attributes]],
            mocked_objects=[mock_toe_inputs_model_add],
            module_at_test=MODULE_AT_TEST,
            paths_list=["toe_inputs_model.add"],
        )
    else:
        mocked_objects, mocked_paths = [
            [
                mock_roots_domain_get_root,
                mock_validate_component,
                mock_toe_inputs_model_add,
            ],
            [
                "roots_domain.get_root",
                "validate_component",
                "toe_inputs_model.add",
            ],
        ]
        mocks_args: list[list[Any]] = [
            [attributes.unreliable_root_id, group_name],
            [attributes.unreliable_root_id, group_name, component],
            [group_name, component, entry_point, attributes],
        ]
        assert set_mocks_return_values(
            mocks_args=mocks_args,
            mocked_objects=mocked_objects,
            module_at_test=MODULE_AT_TEST,
            paths_list=mocked_paths,
        )
    loaders = get_new_context()
    await add(
        loaders=loaders,
        entry_point=entry_point,
        component=component,
        group_name=group_name,
        attributes=attributes,
        is_moving_toe_input=is_moving_toe_input,
    )
    if is_moving_toe_input:
        assert mock_toe_inputs_model_add.called
    else:
        assert all(
            mock_object.called is True for mock_object in mocked_objects
        )


@pytest.mark.parametrize(
    [
        "current_value",
    ],
    [
        [
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
                        "2023-02-17T23:17:11+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    ),
                    seen_first_time_by="new@test.com",
                    unreliable_root_id="",
                ),
            )
        ],
    ],
)
@patch(MODULE_AT_TEST + "toe_inputs_model.remove", new_callable=AsyncMock)
async def test_delete(
    mock_toe_inputs_model_remove: AsyncMock, current_value: ToeInput
) -> None:

    assert set_mocks_return_values(
        mocks_args=[
            [
                current_value.entry_point,
                current_value.component,
                current_value.group_name,
                current_value.state.unreliable_root_id,
            ]
        ],
        mocked_objects=[mock_toe_inputs_model_remove],
        module_at_test=MODULE_AT_TEST,
        paths_list=["toe_inputs_model.remove"],
    )
    await remove(current_value)
    mock_toe_inputs_model_remove.assert_called_with(
        entry_point=current_value.entry_point,
        component=current_value.component,
        group_name=current_value.group_name,
        root_id=current_value.state.unreliable_root_id,
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

    await update(
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
