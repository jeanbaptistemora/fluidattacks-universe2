from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    InvalidFileType,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    files as files_utils,
    logs as logs_utils,
)
from newutils.utils import (
    resolve_kwargs,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Any,
)
from vulnerability_files import (
    domain as vuln_files_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    success = False
    finding_id = kwargs["finding_id"]
    file_input = kwargs["file"]
    finding_loader = info.context.loaders.finding
    finding_data = await finding_loader.load(finding_id)
    group_name = resolve_kwargs(finding_data)
    allowed_mime_type = await files_utils.assert_uploaded_file_mime(
        file_input, ["text/x-yaml", "text/plain", "text/html"]
    )
    group = await info.context.loaders.group.load(group_name)
    organization = await info.context.loaders.organization.load(
        group["organization"]
    )
    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=organization["name"],
        finding_name=finding_data["title"].split(".")[0].lower(),
    )
    if file_input and allowed_mime_type:
        success = await vuln_files_domain.upload_file(
            info,
            file_input,
            finding_data,
            finding_policy,
            support_roots=group["subscription"] == "continuous",
        )
    else:
        raise InvalidFileType()
    if success:
        info.context.loaders.finding.clear(finding_id)
        info.context.loaders.finding_vulns_all.clear(finding_id)
        info.context.loaders.finding_vulns_nzr.clear(finding_id)
        info.context.loaders.finding_vulns.clear(finding_id)
        await redis_del_by_deps(
            "upload_file",
            finding_id=finding_id,
            group_name=group_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Uploaded file in {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to delete file from {group_name} group",
        )
        raise ErrorUploadingFileS3()
    return SimplePayload(success=success)
