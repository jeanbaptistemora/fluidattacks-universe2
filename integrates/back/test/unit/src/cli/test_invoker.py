from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from cli.invoker import (
    main as invoker_main,
)
import pytest
import sys
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


@pytest.mark.asyncio
@patch(MODULE_AT_TEST + "dynamo_shutdown")
@patch(MODULE_AT_TEST + "dynamo_startup")
async def test_invoker(
    mock_dynamo_startup: AsyncMock,
    mock_dynamo_shutdown: AsyncMock,
) -> None:
    mocked_objects, mocked_paths = [
        [
            mock_dynamo_startup,
            mock_dynamo_shutdown,
        ],
        ["dynamo_shutdown", "dynamo_startup"],
    ]
    mocks_args: list[list[Any]] = [[], []]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    test_args = ["dev", "schedulers.missing_environment_alert.main"]
    with patch.object(sys, "argv", test_args) as mock_sys:
        await invoker_main()
    assert all(mock_object.called is True for mock_object in mocked_objects)
    assert mock_sys[0] == "dev"
