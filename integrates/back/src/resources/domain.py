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
    validations,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    cast,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_file_to_db(
    files_data: list[dict[str, str]],
    group_name: str,
    user_email: str,
) -> bool:
    success = False
    group_name = group_name.lower()
    json_data: list[ResourceType] = []
    for file_info in files_data:
        description = file_info["description"]
        validations.validate_fields(cast(list[str], [description]))
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
    group_files = cast(list[ResourceType], files.get("files", []))
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
