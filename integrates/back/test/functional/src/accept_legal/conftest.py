# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("accept_legal")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "users": [
            {
                "email": "admin@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1634677195,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dcd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c40055253c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "hacker@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1634677195,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07557ec12dcd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716723c40055253c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "reattacker@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657298463,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07667ec12dcd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716731c40055253c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "user@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657298264,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07777ec12dcd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716742c40055253c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "user_manager@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657298299,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dcd7",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c40055253",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "vulnerability_manager@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657298346,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec2dcd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c4005253c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "resourcer@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657298463,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dc07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c4005523c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "reviewer@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657295874,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dcd7",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c4005525c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "service_forces@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657278953,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dc07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c4005523c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
            {
                "email": "customer_manager@gmail.com",
                "first_login": "",
                "first_name": "",
                "access_token": {
                    "iat": 1657287433,
                    "jti": "c8d9d5f095958cf200f7435508fc2dba37d07447ec12dd07",
                    "salt": "27c7f388ccdd7cc432871c84b63e78cd716739c4005553c",
                },
                "last_login": "",
                "last_name": "",
                "legal_remember": True,
                "push_tokens": [],
                "registered": True,
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
