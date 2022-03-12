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


async def add_file(
    files_data: List[Dict[str, str]],
    uploaded_file: UploadFile,
    group_name: str,
    user_email: str,
) -> bool:
    success = False
    group_name = group_name.lower()
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
    file_id = f"{group_name}/{uploaded_file.filename}"
    try:
        file_size = 300
        await validate_file_size(uploaded_file, file_size)
    except InvalidFileSize as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    files = await groups_domain.get_attributes(group_name, ["files"])
    group_files = cast(List[ResourceType], files.get("files", []))
    if group_files:
        contains_repeated = [
            f.get("fileName")
            for f in group_files
            if f.get("fileName") == uploaded_file.filename
        ]
        if contains_repeated:
            LOGGER.error("File already exists", **NOEXTRA)
    else:
        # Group doesn't have files
        pass
    if validations.validate_file_name(uploaded_file.filename):
        group_files.extend(json_data)
        await resources_utils.save_file(uploaded_file, file_id)
        success = groups_domain.update(group_name, {"files": group_files})
    return success


async def remove_file(file_name: str, group_name: str) -> bool:
    success = False
    group_name = group_name.lower()
    group = await groups_domain.get_attributes(group_name, ["files"])
    file_list = cast(List[Dict[str, str]], group.get("files", []))
    index = -1
    cont = 0
    while index < 0 and len(file_list) > cont:
        index = cont if file_list[cont]["fileName"] == file_name else -1
        cont += 1
    if index >= 0:
        file_url = f"{group_name.lower()}/{file_name}"
        await resources_utils.remove_file(file_url)
        success = await resources_dal.remove(group_name, "files", index)
    return success


async def validate_file_size(
    uploaded_file: UploadFile, file_size: int
) -> bool:
    """Validate if uploaded file size is less than a given file size."""
    mib = 1048576
    if await files_utils.get_file_size(uploaded_file) > file_size * mib:
        raise InvalidFileSize()
    return True


async def add_file_to_db(
    files_data: List[Dict[str, str]],
    group_name: str,
    user_email: str,
) -> bool:
    success = False
    group_name = group_name.lower()
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
    files = await groups_domain.get_attributes(group_name, ["files"])
    group_files = cast(List[ResourceType], files.get("files", []))
    if group_files:
        contains_repeated = [
            f.get("fileName")
            for f in group_files
            if f.get("fileName") == files_data[0]["fileName"]
        ]
        if contains_repeated:
            LOGGER.error("File already exists", **NOEXTRA)
    else:
        # Group doesn't have files
        pass
    if validations.validate_file_name(files_data[0]["fileName"]):
        group_files.extend(json_data)
        success = await groups_domain.update(
            group_name, {"files": group_files}
        )

    return success
