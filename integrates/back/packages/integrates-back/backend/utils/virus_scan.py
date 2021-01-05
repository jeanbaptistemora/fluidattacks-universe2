import logging
import tempfile

import cloudmersive_virus_api_client
from cloudmersive_virus_api_client.rest import ApiException
from starlette.datastructures import UploadFile

from backend.exceptions import FileInfected
from back.settings import LOGGING
from __init__ import (
    FI_CLOUDMERSIVE_API_KEY,
    FI_ENVIRONMENT
)

logging.config.dictConfig(LOGGING)

# Constants
API_CONFIGURATION = cloudmersive_virus_api_client.Configuration()
API_CONFIGURATION.api_key['Apikey'] = FI_CLOUDMERSIVE_API_KEY
API_CLIENT = cloudmersive_virus_api_client.ScanApi(
    cloudmersive_virus_api_client.ApiClient(API_CONFIGURATION))
LOGGER = logging.getLogger(__name__)


def scan_file(
        target_file: UploadFile,
        user_email: str,
        project_name: str) -> None:
    if FI_ENVIRONMENT == 'production':
        payload_data = {
            'project_name': project_name,
            'user_email': user_email,
            'target_file_name': target_file.filename
        }
        file_object = target_file.file
        try:
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(file_object.read())
            tmp_file.flush()
            api_response = API_CLIENT.scan_file_advanced(
                tmp_file.name,
                allow_executables=True,
                allow_scripts=True,
                allow_invalid_files=True
            )
            tmp_file.close()
            file_object.seek(0)
            if not api_response.clean_result:
                LOGGER.error('File infected', extra={'extra': payload_data})
                raise FileInfected()
        except ApiException as api_error:
            LOGGER.exception(api_error, extra={'extra': payload_data})
            file_object.seek(0)
