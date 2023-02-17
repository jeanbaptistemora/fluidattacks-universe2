from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    Optional,
    Union,
)

Resource = dict[str, Optional[str]]
Resources = dict[str, Union[str, Optional[list[Resource]]]]


def _format_group_files(group_files: list[GroupFile]) -> list[Resource]:
    return [
        {
            "description": file.description,
            "file_name": file.file_name,
            "uploader": file.modified_by,
            "upload_date": datetime_utils.get_as_str(file.modified_date)
            if file.modified_date
            else None,
        }
        for file in group_files
    ]


@QUERY.field("resources")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> Resources:
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(group_name.lower())

    return {
        "files": _format_group_files(group.files) if group.files else None,
        "group_name": group_name,
    }
