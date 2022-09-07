# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from integrates.graphql import (
    client as graphql_client,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_client(
    test_integrates_api_token: str,
) -> None:
    async with graphql_client() as client:
        # pylint: disable=protected-access
        assert client.session._default_headers == {
            "authorization": f"Bearer {test_integrates_api_token}",
            "x-integrates-source": "skims",
        }
