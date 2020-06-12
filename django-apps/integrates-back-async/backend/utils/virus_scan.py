import tempfile
from typing import IO
import cloudmersive_virus_api_client
import rollbar
from cloudmersive_virus_api_client.rest import ApiException
from backend.exceptions import FileInfected
from __init__ import FI_CLOUDMERSIVE_API_KEY, FI_ENVIRONMENT


API_CONFIGURATION = cloudmersive_virus_api_client.Configuration()
API_CONFIGURATION.api_key['Apikey'] = FI_CLOUDMERSIVE_API_KEY
API_CLIENT = cloudmersive_virus_api_client.ScanApi(
    cloudmersive_virus_api_client.ApiClient(API_CONFIGURATION))


def scan_file(file_object: IO):
    if FI_ENVIRONMENT == 'production':
        try:
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(file_object.read())
            tmp_file.flush()
            api_response = API_CLIENT.scan_file_advanced(tmp_file.name,
                                                         allow_executables=True,
                                                         allow_scripts=True)
            tmp_file.close()
            file_object.seek(0)
            if not api_response.clean_result:
                raise FileInfected()
        except ApiException as api_error:
            rollbar.report_message('Error: Cloudmersive VirusScan API error: %s' % api_error)
