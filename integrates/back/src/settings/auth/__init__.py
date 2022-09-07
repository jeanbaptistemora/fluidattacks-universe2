# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .azure import (
    AZURE_ARGS,
)
from .bitbucket import (
    BITBUCKET_ARGS,
)
from .google import (
    GOOGLE_ARGS,
)
from authlib.integrations.starlette_client import (
    OAuth,
)

OAUTH = OAuth()
OAUTH.register(**AZURE_ARGS)
OAUTH.register(**GOOGLE_ARGS)
OAUTH.register(**BITBUCKET_ARGS)

__all__ = ["AZURE_ARGS", "BITBUCKET_ARGS", "GOOGLE_ARGS", "OAUTH"]
