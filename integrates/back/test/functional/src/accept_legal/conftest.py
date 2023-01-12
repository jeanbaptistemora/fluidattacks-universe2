# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderAccessToken,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Dict,
)


@pytest.mark.resolver_test_group("accept_legal")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "stakeholders": [
            Stakeholder(
                email="admin@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1634677195,
                    jti="c8d9d5f095958cf200f7435508fc2dba37d047ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e78cd7139c40055253c",
                ),
            ),
            Stakeholder(
                email="hacker@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1634677195,
                    jti="c8d9d5f095958cf200f7435508fc2d37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e7d716739c40055253c",
                ),
            ),
            Stakeholder(
                email="reattacker@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657298463,
                    jti="c8d9d5f095958cf200f7435508fc2d37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e7d716739c40055253c",
                ),
            ),
            Stakeholder(
                email="user@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657298264,
                    jti="c8d9d5f095958cf200f7435508fcba37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871cb63e78cd716739c40055253c",
                ),
            ),
            Stakeholder(
                email="user_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657298299,
                    jti="c8d9d5f095958cf200f743550c2dba37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c863e78cd716739c40055253c",
                ),
            ),
            Stakeholder(
                email="vulnerability_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657298346,
                    jti="c8d9d5f095958cf200f7435508fc2a37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63ecd716739c40055253c",
                ),
            ),
            Stakeholder(
                email="resourcer@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657298463,
                    jti="c8d9d5f095958cf200f7435508fc2a37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b678cd716739c40055253c",
                ),
            ),
            Stakeholder(
                email="reviewer@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657295874,
                    jti="c8d9d5f095958cf200f7435508fc2db7d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e7d716739c40055253c",
                ),
            ),
            Stakeholder(
                email="service_forces@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657278953,
                    jti="c8d9d5f095958cf200f7435508fc2d37d07447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e7d716739c40055253c",
                ),
            ),
            Stakeholder(
                email="customer_manager@gmail.com",
                legal_remember=True,
                is_registered=True,
                access_token=StakeholderAccessToken(
                    iat=1657287433,
                    jti="c8d9d5f095958cf200f7435508fc2dba37d447ec12dcd07",
                    salt="27c7f388ccdd7cc432871c84b63e78cd7139c40055253c",
                ),
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
