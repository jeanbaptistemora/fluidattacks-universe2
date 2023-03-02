from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from db_model.stakeholders.get import (
    StakeholderLoader,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email", "email_not_found"],
    [["integratesmanager@fluidattacks.com", "testanewuser@test.test"]],
)
@patch(
    MODULE_AT_TEST + "_get_stakeholders_no_fallback", new_callable=AsyncMock
)
async def test_stakeholderloader(
    mock__get_stakeholders_no_fallback: AsyncMock,
    email: str,
    email_not_found: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[email]],
        mocked_objects=[mock__get_stakeholders_no_fallback],
        module_at_test=MODULE_AT_TEST,
        paths_list=["_get_stakeholders_no_fallback"],
    )

    loaders = StakeholderLoader()
    stakeholder = await (loaders.load(email))
    assert isinstance(stakeholder, Stakeholder)
    assert stakeholder.role == "admin"
    assert mock__get_stakeholders_no_fallback.call_count == 1

    mock__get_stakeholders_no_fallback.return_value = [None]
    non_existent_stakeholder = await (loaders.load(email_not_found))
    assert not isinstance(non_existent_stakeholder, Stakeholder)
    assert not non_existent_stakeholder
    assert mock__get_stakeholders_no_fallback.call_count == 2
