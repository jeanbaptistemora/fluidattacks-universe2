# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    timedelta,
)
from db_model.stakeholders.types import (
    StakeholderAccessToken,
)
from newutils import (
    token as token_utils,
)
from sessions import (
    utils as sessions_utils,
)
from settings import (
    SESSION_COOKIE_AGE,
)
from time import (
    time,
)

AGE_WEEKS = 27  # invalid expiration time


def test_verificate_hash_token() -> None:
    token = token_utils.calculate_hash_token()
    access_token = StakeholderAccessToken(
        iat=0, salt=token["salt"], jti=token["jti_hashed"]
    )
    different_token = token_utils.calculate_hash_token()

    assert token_utils.verificate_hash_token(access_token, token["jti"])
    assert not token_utils.verificate_hash_token(
        access_token, different_token["jti"]
    )


def test_is_valid_expiration_time() -> None:
    exp_valid = int(time()) + SESSION_COOKIE_AGE
    exp_invalid = int(time() + timedelta(weeks=AGE_WEEKS).total_seconds())

    assert sessions_utils.is_valid_expiration_time(exp_valid)
    assert not sessions_utils.is_valid_expiration_time(exp_invalid)
