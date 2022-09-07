# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_AZUREAD_OAUTH2_KEY,
    FI_AZUREAD_OAUTH2_SECRET,
)

BASE_URL = "https://login.microsoftonline.com"
AZURE_CONF_URL = f"{BASE_URL}/common/v2.0/.well-known/openid-configuration"

AZURE_ARGS = dict(
    name="azure",
    client_id=FI_AZUREAD_OAUTH2_KEY,
    client_secret=FI_AZUREAD_OAUTH2_SECRET,
    server_metadata_url=AZURE_CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)
