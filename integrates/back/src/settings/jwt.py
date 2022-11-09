# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)

JWT_COOKIE_NAME = "integrates_session"
JWT_COOKIE_SAMESITE = "Lax"
JWT_SECRET = FI_JWT_SECRET
JWT_SECRET_API = FI_JWT_SECRET_API
