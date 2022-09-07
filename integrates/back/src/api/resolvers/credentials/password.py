# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.credentials.types import (
    Credentials,
    HttpsSecret,
)
from decorators import (
    enforce_owner,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@enforce_owner
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> Optional[str]:
    return (
        parent.state.secret.password
        if isinstance(parent.state.secret, HttpsSecret)
        else None
    )
