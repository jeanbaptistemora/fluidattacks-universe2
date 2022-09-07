# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_GOOGLE_OAUTH2_KEY,
    FI_GOOGLE_OAUTH2_SECRET,
)

GOOGLE_CONF_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
GOOGLE_USERINFO_ENDPOINT_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

GOOGLE_ARGS = dict(
    name="google",
    client_id=FI_GOOGLE_OAUTH2_KEY,
    client_secret=FI_GOOGLE_OAUTH2_SECRET,
    server_metadata_url=GOOGLE_CONF_URL,
    userinfo_endpoint=GOOGLE_USERINFO_ENDPOINT_URL,
    client_kwargs={"scope": "openid email profile"},
)
