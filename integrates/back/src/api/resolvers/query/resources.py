from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Resources,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupFile,
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
from newutils.datetime import (
    convert_from_iso_str,
)
from newutils.utils import (
    get_key_or_fallback,
    get_present_key,
)
from typing import (
    Dict,
    List,
)


def _format_group_files(group_files: List[GroupFile]) -> List[Dict[str, str]]:
    return [
        {
            "description": file.description,
            "file_name": file.file_name,
            "uploader": file.modified_by,
            "upload_date": convert_from_iso_str(file.modified_date)
            if file.modified_date
            else None,
        }
        for file in group_files
    ]


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Resources:
    group_name: str = str(get_key_or_fallback(kwargs)).lower()
    group_name_key = get_present_key(kwargs)
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group_typed.load(group_name)

    return {
        "files": _format_group_files(group.files) if group.files else None,
        f"{group_name_key}": group_name,
    }
