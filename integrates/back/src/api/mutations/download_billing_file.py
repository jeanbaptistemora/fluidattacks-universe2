# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from api.mutations import (
    DownloadFilePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    payment_method_id: str,
    file_name: str,
    **kwargs: Any,
) -> DownloadFilePayload:
    org: Organization = await info.context.loaders.organization.load(
        kwargs["organization_id"],
    )
    success = False
    signed_url = await billing_domain.get_document_link(
        org, payment_method_id, file_name
    )
    if signed_url:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Downloaded file in payment method {payment_method_id}"
            + "successfully",
        )
        success = True
    else:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to download file in payment method"
            + "{payment_method_id}",
        )
    return DownloadFilePayload(success=success, url=signed_url)
