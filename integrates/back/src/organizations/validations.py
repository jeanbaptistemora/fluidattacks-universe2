# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    CredentialAlreadyExists,
)
from db_model.credentials.types import (
    Credentials,
)
from typing import (
    Any,
)


async def validate_credentials_name_in_organization(
    loaders: Any,
    organization_id: str,
    credentials_name: str,
) -> None:
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization_id)
    credentials_names = {
        credentials.state.name.strip() for credentials in org_credentials
    }
    if credentials_name.strip() in credentials_names:
        raise CredentialAlreadyExists()
