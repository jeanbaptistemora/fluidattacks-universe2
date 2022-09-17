# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from stakeholders import (
    domain as stakeholders_domain,
)
from stakeholders.domain import (
    has_valid_access_token,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_add_push_token() -> None:
    loaders: Dataloaders = get_new_context()
    user_email = "unittest@fluidattacks.com"
    valid_token = "ExponentPushToken[something123]"
    await stakeholders_domain.add_push_token(loaders, user_email, valid_token)

    loaders = get_new_context()
    user_attrs: Stakeholder = await loaders.stakeholder.load(user_email)
    assert valid_token in user_attrs.push_tokens  # type: ignore


async def test_exists() -> None:
    loaders: Dataloaders = get_new_context()
    assert await stakeholders_domain.exists(
        loaders=loaders, email="integratesuser@gmail.com"
    )
    assert not await stakeholders_domain.exists(
        loaders=loaders, email="madeup_stakeholder@void.com"
    )


async def test_has_valid_access_token() -> None:
    loaders = get_new_context()
    jti = "ff6273146a0e4ed82715cdb4db7f5915b30dfa4bccc54c0d2cda17a61a44a5f6"
    assert await has_valid_access_token(
        loaders,
        "unittest@fluidattacks.com",
        {"test_context": "test_context_value"},
        jti,
    )
