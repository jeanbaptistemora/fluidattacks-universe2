import cloudmersive_virus_api_client
from context import (
    FI_CLOUDMERSIVE_API_KEY,
    FI_ENVIRONMENT,
)
import logging
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
import tempfile

logging.config.dictConfig(LOGGING)

# Constants
API_CONFIGURATION = cloudmersive_virus_api_client.Configuration()
API_CONFIGURATION.api_key["Apikey"] = FI_CLOUDMERSIVE_API_KEY
API_CLIENT = cloudmersive_virus_api_client.ScanApi(
    cloudmersive_virus_api_client.ApiClient(API_CONFIGURATION)
)
LOGGER = logging.getLogger(__name__)


# pylint: disable=consider-using-with
def scan_file(
    target_file: UploadFile, file_name: str, user_email: str, group_name: str
) -> bool:
    success = False
    if FI_ENVIRONMENT == "production":
        payload_data = {
            "group_name": group_name,
            "user_email": user_email,
            "target_file_name": file_name,
        }
        file_object = target_file
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.write(file_object.read())
        tmp_file.flush()
        api_response = API_CLIENT.scan_file_advanced(
            tmp_file.name,
            allow_executables=True,
            allow_macros=True,
            allow_scripts=True,
            allow_invalid_files=True,
        )
        tmp_file.close()
        file_object.seek(0)
        if api_response.clean_result:
            success = True
        elif not api_response.clean_result:
            LOGGER.error("File infected", extra={"extra": payload_data})

    return success
