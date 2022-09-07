# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.types import (
    Event,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_event() -> None:
    loaders: Dataloaders = get_new_context()
    event_id = "418900971"
    test_data: Event = await loaders.event.load(event_id)
    expected_output = "unittesting"
    assert test_data.group_name == expected_output
