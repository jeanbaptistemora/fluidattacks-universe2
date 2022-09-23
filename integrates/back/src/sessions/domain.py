# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
    StateSessionType,
)
from typing import (
    Any,
    Dict,
)


async def remove_session_token(content: Dict[str, Any], email: str) -> None:
    """Revoke session token attribute"""
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=content["jti"],
                state=StateSessionType.REVOKED,
            ),
        ),
        email=email,
    )


async def verify_session_token(content: Dict[str, Any], email: str) -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    if stakeholder.session_token:
        if stakeholder.session_token.state == StateSessionType.REVOKED:
            raise ExpiredToken()

        if stakeholder.session_token.jti != content["jti"]:
            await remove_session_token(content, email)
            raise ExpiredToken()
    else:
        raise InvalidAuthorization()
