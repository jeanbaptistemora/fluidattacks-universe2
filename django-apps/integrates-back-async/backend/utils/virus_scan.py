import tempfile
from typing import IO
import cloudmersive_virus_api_client
import rollbar
from cloudmersive_virus_api_client.rest import ApiException
from backend.exceptions import FileInfected
from __init__ import FI_CLOUDMERSIVE_API_KEY


API_CLIENT = cloudmersive_virus_api_client.ScanApi()
API_CLIENT.api_client.configuration.api_key = {}
API_CLIENT.api_client.configuration.api_key['Apikey'] = FI_CLOUDMERSIVE_API_KEY


def scan_file(file_object: IO):
    try:
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.write(file_object.read())
        api_response = API_CLIENT.scan_file(tmp_file.name)
        if not api_response.clean_result:
            raise FileInfected()
    except ApiException:
        rollbar.report_message('Error: Cloudmersive VirusScan API error')
