# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> bool:
    return isinstance(parent.state.secret, HttpsPatSecret)
