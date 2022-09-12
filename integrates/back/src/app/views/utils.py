# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    UserAccessInfo,
)
from typing import (
    Dict,
)


def format_user_access_info(user: Dict[str, str]) -> UserAccessInfo:
    return UserAccessInfo(
        first_name=user.get("given_name", ""),
        last_name=user.get("family_name", ""),
        user_email=user["email"],
    )
