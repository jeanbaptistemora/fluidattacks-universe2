"""Domain functions for resources."""


from aioextensions import (
    collect,
)
from custom_exceptions import (
    InvalidFileSize,
)
from custom_types import (
    Resource as ResourceType,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
    files as files_utils,
    resources as resources_utils,
    validations,
)
from resources import (
    dal as resources_dal,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    cast,
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def create_file(
    files_data: List[Dict[str, str]],
    uploaded_file: UploadFile,
    project_name: str,
    user_email: str,
) -> bool:
    success = False
    project_name = project_name.lower()
    json_data: List[ResourceType] = []
    for file_info in files_data:
        description = file_info["description"]
        validations.validate_fields(cast(List[str], [description]))
        validations.validate_field_length(description, 200)
        json_data.append(
            {
                "fileName": file_info.get("fileName", file_info["fileName"]),
                "description": description,
                "uploadDate": datetime_utils.get_as_str(
                    datetime_utils.get_now(), date_format="%Y-%m-%d %H:%M"
                ),
                "uploader": user_email,
            }
        )
    file_id = f"{project_name}/{uploaded_file.filename}"
    try:
        file_size = 300
        await validate_file_size(uploaded_file, file_size)
    except InvalidFileSize as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    files = await groups_domain.get_attributes(project_name, ["files"])
    project_files = cast(List[ResourceType], files.get("files", []))
    if project_files:
        contains_repeated = [
            f.get("fileName")
            for f in project_files
            if f.get("fileName") == uploaded_file.filename
        ]
        if contains_repeated:
            LOGGER.error("File already exists", **NOEXTRA)
    else:
        # Group doesn't have files
        pass
    if validations.validate_file_name(uploaded_file.filename):
        project_files.extend(json_data)
        success = all(
            await collect(
                [
                    resources_utils.save_file(uploaded_file, file_id),
                    groups_domain.update(
                        project_name, {"files": project_files}
                    ),
                ]
            )
        )
    return success


async def remove_file(file_name: str, project_name: str) -> bool:
    success = False
    project_name = project_name.lower()
    project = await groups_domain.get_attributes(project_name, ["files"])
    file_list = cast(List[Dict[str, str]], project.get("files", []))
    index = -1
    cont = 0
    while index < 0 and len(file_list) > cont:
        if file_list[cont]["fileName"] == file_name:
            index = cont
        else:
            index = -1
        cont += 1
    if index >= 0:
        file_url = f"{project_name.lower()}/{file_name}"
        success = all(
            await collect(
                [
                    resources_utils.remove_file(file_url),
                    resources_dal.remove(project_name, "files", index),
                ]
            )
        )
    return success


async def validate_file_size(
    uploaded_file: UploadFile, file_size: int
) -> bool:
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    if await files_utils.get_file_size(uploaded_file) > file_size * mib:
        raise InvalidFileSize()
    return True
