# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.enums import (
    CredentialType,
)
from typing import (
    NamedTuple,
    Optional,
)


class CredentialAttributesToAdd(NamedTuple):
    name: str
    key: Optional[str]
    token: Optional[str]
    type: CredentialType
    user: Optional[str]
    password: Optional[str]
    is_pat: Optional[bool] = False
    azure_organization: Optional[str] = None


class CredentialAttributesToUpdate(NamedTuple):
    name: Optional[str]
    key: Optional[str]
    token: Optional[str]
    type: Optional[CredentialType]
    user: Optional[str]
    password: Optional[str]
    is_pat: Optional[bool] = False
    azure_organization: Optional[str] = None
