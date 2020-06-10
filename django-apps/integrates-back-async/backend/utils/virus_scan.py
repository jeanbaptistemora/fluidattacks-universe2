import rollbar
import cloudmersive_virus_api_client
from cloudmersive_virus_api_client.rest import ApiException
from backend.exceptions import FileInfected
from __init__ import FI_CLOUDMERSIVE_API_KEY


API_CLIENT = cloudmersive_virus_api_client.ScanApi()
API_CLIENT.api_client.configuration.api_key = {}
API_CLIENT.api_client.configuration.api_key['Apikey'] = FI_CLOUDMERSIVE_API_KEY


def scan_file(file_path: str):
    try:
        api_response = API_CLIENT.scan_file(file_path)
        if not api_response.clean_result:
            raise FileInfected()
    except ApiException:
        rollbar.report_message('Error: Cloudmersive VirusScan API error')
