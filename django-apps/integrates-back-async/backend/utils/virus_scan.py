import tempfile
import cloudmersive_virus_api_client
import rollbar
from cloudmersive_virus_api_client.rest import ApiException
from backend.exceptions import FileInfected
from django.core.files.uploadedfile import InMemoryUploadedFile
from __init__ import FI_CLOUDMERSIVE_API_KEY, FI_ENVIRONMENT


API_CONFIGURATION = cloudmersive_virus_api_client.Configuration()
API_CONFIGURATION.api_key['Apikey'] = FI_CLOUDMERSIVE_API_KEY
API_CLIENT = cloudmersive_virus_api_client.ScanApi(
    cloudmersive_virus_api_client.ApiClient(API_CONFIGURATION))


def scan_file(target_file: InMemoryUploadedFile, user_email: str, project_name: str):
    if FI_ENVIRONMENT == 'production':
        try:
            file_object = target_file.file
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(file_object.read())
            tmp_file.flush()
            api_response = API_CLIENT.scan_file_advanced(
                tmp_file.name,
                allow_executables=True,
                allow_scripts=True,
                allow_invalid_files=True)
            tmp_file.close()
            file_object.seek(0)
            if not api_response.clean_result:
                rollbar.report_message(
                    f'Report: Cloudmersive VirusScan file infected for user '
                    f'{user_email} in project {project_name}: '
                    f'{target_file.name}\n{str(api_response)}')
                raise FileInfected()
        except ApiException as api_error:
            rollbar.report_message(
                f'Error: Cloudmersive VirusScan API error for user '
                f'{user_email} in project {project_name}: {api_error}')
