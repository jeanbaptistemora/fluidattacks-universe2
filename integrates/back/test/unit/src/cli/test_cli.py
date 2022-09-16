# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from cli.invoker import (
    main as invoker_main,
)
import pytest
import sys
from typing import (
    Any,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@mock.patch("cli.invoker.dynamo_startup")
@mock.patch("cli.invoker.dynamo_shutdown")
async def test_invoker(
    dynamo_shutdown_mock: Any,
    dynamo_startup_mock: Any,
) -> None:
    dynamo_startup_mock.return_value = None
    dynamo_shutdown_mock.return_value = None
    test_args = ["dev", "schedulers.missing_environment_alert.main"]
    with mock.patch.object(sys, "argv", test_args) as mock_sys:
        await invoker_main()
    assert dynamo_shutdown_mock.called is True
    assert dynamo_startup_mock.called is True
    assert mock_sys[0] == "dev"
