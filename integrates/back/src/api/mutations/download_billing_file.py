from .payloads.types import (
    DownloadFilePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from custom_exceptions import (
    ErrorDownloadingFile,
)
from dataloaders import (
    Dataloaders,
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
from organizations import (
    utils as orgs_utils,
)
from typing import (
    Any,
)


@MUTATION.field("downloadBillingFile")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    payment_method_id: str,
    file_name: str,
    **kwargs: Any,
) -> DownloadFilePayload:
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, kwargs["organization_id"]
    )
    signed_url = await billing_domain.get_document_link(
        organization, payment_method_id, file_name
    )
    if signed_url:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Downloaded file in payment method {payment_method_id}"
            + "successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to download file in payment method"
            + f"{payment_method_id}",
        )
        raise ErrorDownloadingFile()

    return DownloadFilePayload(success=True, url=signed_url)
