# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    in_thread,
)
from context import (
    FI_ENVIRONMENT,
)
from mixpanel import (
    Mixpanel,
)
from settings import (
    MIXPANEL_API_TOKEN,
)


async def mixpanel_track(email: str, event: str, **extra: str) -> None:
    if FI_ENVIRONMENT == "production":
        await in_thread(
            Mixpanel(MIXPANEL_API_TOKEN).track,
            email,
            event,
            {"integrates_user_email": email, **extra},
        )
