from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidFileType,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    files as files_utils,
    logs as logs_utils,
)
from organizations.utils import (
    get_organization,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from typing import (
    Any,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerability_files import (
    domain as vuln_files_domain,
)


@MUTATION.field("uploadFile")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_report_vulnerabilities,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    try:
        finding_id = kwargs["finding_id"]
        file_input = kwargs["file"]
        loaders: Dataloaders = info.context.loaders
        finding = await findings_domain.get_finding(loaders, finding_id)
        allowed_mime_type = await files_utils.assert_uploaded_file_mime(
            file_input, ["text/x-yaml", "text/plain", "text/html"]
        )
        group = await groups_domain.get_group(loaders, finding.group_name)
        organization = await get_organization(loaders, group.organization_id)
        finding_policy = await policies_domain.get_finding_policy_by_name(
            loaders=loaders,
            finding_name=finding.title.lower(),
            organization_name=organization.name,
        )
        if file_input and allowed_mime_type:
            processed_vulnerabilities = await vuln_files_domain.upload_file(
                info,
                file_input,
                finding_id,
                finding_policy,
                finding.group_name,
            )
        else:
            raise InvalidFileType()
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding_id],
            vulnerability_ids=list(processed_vulnerabilities),
        )
        if finding_policy:
            await update_unreliable_indicators_by_deps(
                EntityDependency.handle_finding_policy,
                finding_ids=[finding_id],
                vulnerability_ids=list(processed_vulnerabilities),
            )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Uploaded file in {finding.group_name} group "
            "successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to upload file in {finding.group_name} "
            "group",
        )
        raise

    return SimplePayload(success=True)
